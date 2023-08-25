import streamlit as st
from streamlit_chat import message
from data_utils import load_data
from recommendation import initialize_recommendations, get_hybrid_recommendations

folder_path = 'Pages Preprocessed'
df = load_data(folder_path)
initialize_recommendations(df)
class ChatHistory:
        
    def __init__(self):
        self.history = st.session_state.get("history", [])
        st.session_state["history"] = self.history

    def default_greeting(self):
        return "Hey 👋, how can I help you ?"

    def initialize_user_history(self):
        if "user" not in st.session_state:
            st.session_state["user"] = []

    def initialize_assistant_history(self):
        if "assistant" not in st.session_state:
            st.session_state["assistant"] = [self.default_greeting()]

    def initialize(self):
        self.initialize_user_history()
        self.initialize_assistant_history()

    def append(self, mode, message):
        st.session_state[mode].append(message)

    def generate_messages(self, container):
        if st.session_state["assistant"]:
            with container:
                for i in range(len(st.session_state["assistant"])):
                    if i < len(st.session_state["user"]):
                        message(
                            st.session_state["user"][i],
                            is_user=True,
                            key=f"history_{i}_user",
                            avatar_style="big-smile",
                        )
                    message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")



def chat_interface():
    # Instantiate the ChatHistory class
    history = ChatHistory()
    
    st.title("Hybrid Recommendation Chatbot")

    # Initialize chat history
    history.initialize()

    with st.container():
        response_container = st.container()

    # Create containers for chat responses and user prompts
    response_container, prompt_container = st.container(), st.container()

    # Display the initial greeting from the chatbot
    with response_container:
        message(st.session_state["assistant"][0], key="initial_greeting", avatar_style="thumbs")

    with st.container():
            user_input = st.text_input("You: ", "")
    # Create a dropdown menu for selecting the number of recommendations
    num_recommendations = st.selectbox("Select number of recommendations", [1, 5, 10, 15, 20], index=1) # Change index to change default number of recommendations

    if user_input:
        if user_input.lower() == 'exit':
            st.write("Goodbye!")
        else:
            recommendations = get_hybrid_recommendations(df, user_input, top_n=num_recommendations)


            # Determine the type of recommendation message based on user query
            if any(word in user_input.lower() for word in ["what", "where", "how", "when"]):
                response_msg = "Based on your query, here are some recommendations:\n"
            else:
                response_msg = "Here are some suggestions for you:\n"

            if not recommendations.empty:
                links = []
                for idx, row in recommendations.iterrows():
                    if row['Title']:
                        title = row['Title']
                    elif row['Subtitle']:
                        title = row['Subtitle']
                    elif row['Summary']:
                        title = row['Summary']
                    elif row['Question']:
                        title = row['Question']
                    elif row['Tags']:
                        title = row['Tags']
                    else:
                        title = row['Search Term']

                    # title = row['Title'] if row['Title'] else 'Title'
                    # subtitle = row['Subtitle'] if row['Subtitle'] else 'Subtitle'
                    # summary = row['Summary'] if row['Summary'] else 'Summary'
                    # question = row['Question'] if row['Question'] else 'Question'
                    # tags = row['Tags'] if row['Tags'] else 'Tags'
                    # search_term = row['Search Term'] if row['Search Term'] else 'Search Term'

                    # st.write(f"- {title} | {subtitle} | {summary} | {question} | {tags} | {search_term} - ({row['URL']})")

                    links.append(f"{idx +1} - {title}\nLink: [{row['URL']}]({row['URL']})\n")
                
                # Combine all links into a single response message
                response_msg += "\n".join(links)
            else:
                response_msg += "Sorry, I couldn't find any recommendations based on your query."
            
            # Update the chat history
            history.append("user", user_input)
            history.append("assistant", response_msg)
            
            with response_container:
                # Display the chat messages excluding the initial greeting
                for i in range(1, len(st.session_state["assistant"])):
                    message(st.session_state["user"][i-1], is_user=True, key=f"history_{i-1}_user", avatar_style="big-smile")
                    message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")

if __name__ == "__main__":
    chat_interface()
