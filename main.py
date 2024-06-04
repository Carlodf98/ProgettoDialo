import pygame
import openai
from transformers import AutoModelForCausalLM, AutoTokenizer


class SimpleChatbot:
    def __init__(self, openai_api_key):

        self.model_name = "abhiramtirumala/DialoGPT-sarcastic-medium"


        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

        openai.api_key = openai_api_key

    def get_chatgpt_response(self, user_input):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"Error in getting response from ChatGPT: {e}")
            return "Sorry, I'm having trouble connecting to the ChatGPT service."


    def transform_with_dialoGPT(self, text):
        try:
            new_user_input_ids = self.tokenizer.encode(text + self.tokenizer.eos_token, return_tensors='pt')
            chat_history_ids = new_user_input_ids
            response_ids = self.model.generate(chat_history_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)
            response = self.tokenizer.decode(response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
            return response
        except Exception as e:
            print(f"Error in transforming response with DialoGPT: {e}")
            return "Sorry, I'm having trouble generating a sarcastic response."

    def get_response(self, user_input):
        chatgpt_response = self.get_chatgpt_response(user_input)
        if "Sorry, I'm having trouble" in chatgpt_response:
            return chatgpt_response
        sarcastic_response = self.transform_with_dialoGPT(chatgpt_response)
        combined_response = f"{chatgpt_response} {sarcastic_response}"
        return combined_response


class ChatbotGUI:
    def __init__(self, openai_api_key):
        pygame.init()

        self.screen = pygame.display.set_mode((1600, 1200))
        pygame.display.set_caption('Greed Chatbot')


        icon = pygame.image.load('pc_icon.png')
        pygame.display.set_icon(icon)


        self.BACKGROUND_COLOR = (255, 255, 255)  
        self.TEXT_COLOR = (0, 0, 0)  
        self.BORDER_COLOR = (32, 32, 32)  
        self.BUTTON_COLOR = (0, 204, 85)  
        self.BUTTON_TEXT_COLOR = (0, 0, 0) 
        self.CHAT_WINDOW_COLOR = (204, 255, 204)
        self.INPUT_BOX_COLOR = (255, 255, 255) 


        self.font = pygame.font.Font(None, 24) 
        self.title_font = pygame.font.Font(None, 34) 

        self.input_rect = pygame.Rect(10, 820, 1400, 60)
        self.input_text = ''

        self.chat_history = []


        self.bot_response = ''


        self.send_button_rect = pygame.Rect(1450, 820, 140, 60)


        self.chat_window_rect = pygame.Rect(10, 10, 1580, 800)


        self.chatbot = SimpleChatbot(openai_api_key)


    def draw_text(self, text, font, color, surface, x, y, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)

        y_offset = y
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(topleft=(x, y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += font.get_linesize() + 2

        return y_offset  


    def handle_input(self):
        if self.input_text.strip():  
            self.bot_response = self.chatbot.get_response(self.input_text)
            self.chat_history.append(f"Utente: {self.input_text}")
            self.chat_history.append(f"Bot: {self.bot_response}")
            self.input_text = ''


    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.handle_input()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.send_button_rect.collidepoint(event.pos):
                    self.handle_input()
                if event.type == pygame.TEXTINPUT:
                    self.input_text += event.text


            self.screen.fill(self.BACKGROUND_COLOR)

            pygame.draw.rect(self.screen, self.CHAT_WINDOW_COLOR, self.chat_window_rect)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.chat_window_rect, 2)

            pygame.draw.rect(self.screen, self.INPUT_BOX_COLOR, self.input_rect)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.input_rect, 2)


            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.send_button_rect, 2)

            y_offset = 60  
            for line in self.chat_history[-20:]: 
                y_offset = self.draw_text(line, self.font, self.TEXT_COLOR, self.screen, 20, y_offset, self.chat_window_rect.width - 40)


            self.draw_text("Greed Chatbot", self.title_font, self.TEXT_COLOR, self.screen, 20, 20, self.chat_window_rect.width - 40)


            self.draw_text(self.input_text + '|', self.font, self.TEXT_COLOR, self.screen, self.input_rect.x + 5, self.input_rect.y + 5, self.input_rect.width - 10)

            pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.send_button_rect)
            self.draw_text("Send", self.font, self.BUTTON_TEXT_COLOR, self.screen, self.send_button_rect.x + 50, self.send_button_rect.y + 20, self.send_button_rect.width - 40)


            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    try:

        print("Initializing Chatbot GUI...")
        openai_api_key = "sk-proj-Rfdr3RddodClMmzzR2UpT3BlbkFJ7tuTtPemdleXiPxg2zMH"  
        chatbot_gui = ChatbotGUI(openai_api_key)
        print("Starting Chatbot GUI...")
        chatbot_gui.start()
    except ImportError as e:
        print(f"Error importing required module: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
