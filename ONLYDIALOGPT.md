#TEST 
QUESTO CODICE AVVIA UN PROGRAMMA CHE UTILIZZA SOLO LA VERSIONE DI DIALOGPT.

import pygame
from transformers import AutoModelForCausalLM, AutoTokenizer

# Classe SimpleChatbot per gestire il modello di chatbot
class SimpleChatbot:
    def __init__(self):
        # Nome del modello utilizzato
        self.model_name = "abhiramtirumala/DialoGPT-sarcastic-medium"

        # Carica direttamente il modello e il tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    # Metodo per ottenere la risposta del chatbot
    def get_response(self, user_input):
        # Tokenizza l'input dell'utente e genera una risposta con DialoGPT
        new_user_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = new_user_input_ids

        # Genera la risposta usando il modello
        response_ids = self.model.generate(chat_history_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

# Classe ChatbotGUI per gestire l'interfaccia grafica del chatbot
class ChatbotGUI:
    def __init__(self):
        pygame.init()
        # Imposta la finestra grafica
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Greed Chatbot')

        # Carica e imposta l'icona della finestra
        icon = pygame.image.load('pc_icon.png')
        pygame.display.set_icon(icon)
        # Colori - Palette 
        self.BACKGROUND_COLOR = (255, 255, 255)  # Bianco come sfondo
        self.TEXT_COLOR = (0, 0, 0)  # Testo nero
        self.BORDER_COLOR = (32, 32, 32)  # Grigio più scuro per i bordi
        self.BUTTON_COLOR = (0, 204, 85)  # Verde per i bottoni
        self.BUTTON_TEXT_COLOR = (0, 0, 0)  # Nero per il testo dei bottoni
        self.CHAT_WINDOW_COLOR = (204, 255, 204)  # Verde chiaro quasi bianco per la finestra della chat
        self.INPUT_BOX_COLOR = (255, 255, 255)  # Bianco per la finestra di input
        # Caratteri (Font)
        self.font = pygame.font.Font(None, 27)  # Dimensione del carattere impostata a 27
        self.title_font = pygame.font.Font(None, 36)  # Dimensione del carattere per il titolo
        # Finestra di input
        self.input_rect = pygame.Rect(200, 500, 400, 50)
        self.input_text = ''
        # Storico della chat
        self.chat_history = []
        # Risposta del bot
        self.bot_response = ''
        # Pulsante di invio
        self.send_button_rect = pygame.Rect(620, 500, 80, 50)
        # Finestra della chat
        self.chat_window_rect = pygame.Rect(10, 10, 780, 480)
        # Crea un'istanza del SimpleChatbot
        self.chatbot = SimpleChatbot()

    # Metodo per disegnare il testo sullo schermo
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    # Metodo per gestire l'input dell'utente
    def handle_input(self):
        if self.input_text.strip():  # Verifica che l'input non sia vuoto
            self.bot_response = self.chatbot.get_response(self.input_text)
            self.chat_history.append(f"Utente: {self.input_text}")
            self.chat_history.append(f"Bot: {self.bot_response}")
            self.input_text = ''

    # Metodo per avviare l'interfaccia grafica del chatbot
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
            # Disegna sullo schermo
            self.screen.fill(self.BACKGROUND_COLOR)
            # Disegna la finestra della chat
            pygame.draw.rect(self.screen, self.CHAT_WINDOW_COLOR, self.chat_window_rect)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.chat_window_rect, 2)
            # Disegna la finestra di input
            pygame.draw.rect(self.screen, self.INPUT_BOX_COLOR, self.input_rect) 
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.input_rect, 2)
            # Disegna il pulsante di invio
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.send_button_rect, 2)
            # Visualizza lo storico della chat
            y_offset = 60  # Posiziona il testo dentro la finestra della chat
            for line in self.chat_history[-20:]:  # Mostra solo le ultime 20 righe
                self.draw_text(line, self.font, self.TEXT_COLOR, self.screen, 70, y_offset)
                y_offset += 20
            # Visualizza il titolo finestra della chat 
            self.draw_text("Chatbot", self.title_font, self.TEXT_COLOR, self.screen, 20, 20)
            # Visualizza il testo dell'utente
            self.draw_text(self.input_text + '|', self.font, self.TEXT_COLOR, self.screen, self.input_rect.x + 5, self.input_rect.y + 5)
            # Disegna il pulsante di invio
            pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.send_button_rect)
            # Disegna il testo del pulsante di invio
            self.draw_text("Send", self.font, self.BUTTON_TEXT_COLOR, self.screen, self.send_button_rect.x + 10, self.send_button_rect.y + 10)
            # Aggiorna lo schermo
            pygame.display.flip()

        pygame.quit()

# Sezione principale per verificare se il file è eseguito direttamente
if __name__ == "__main__":
    try:
        # Inizializza e avvia l'interfaccia grafica del chatbot
        print("Initializing Chatbot GUI...")
        chatbot_gui = ChatbotGUI()
        print("Starting Chatbot GUI...")
        chatbot_gui.start()
    except ImportError as e:
        print(f"Error importing required module: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
