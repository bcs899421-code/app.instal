import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time
import os

# --- 1. Definição das Perguntas do Jogo ---
QUESTIONS_DATA = [
    {
        "statement": "Um estudo indica que esperar cerca de 1 hora após acordar para tomar café pode aumentar a disposição e a produtividade ao longo do dia.",
        "image": "images/cafe.jpeg",
        "options": ["REAL", "FAKE"],
        "correct_answer": "REAL",
        "explanation_what": "Existe evidência parcial de que o cortisol (hormônio do estado de alerta) já está naturalmente elevado ao acordar. Consumir café imediatamente pode ter efeito menor, enquanto esperar um pouco pode tornar a cafeína mais eficaz na percepção de energia. No entanto, o efeito não é universal nem extremamente significativo para todas as pessoas.",
        "explanation_how": "Verifique se a informação vem de estudos sobre ritmos circadianos e cortisol. Procure por fontes científicas ou especialistas em sono. Diferencie recomendações baseadas em fisiologia real de promessas exageradas de produtividade.",
        "explanation_red_flags": "Afirmações absolutas como 'sempre aumenta produtividade', ausência de contexto individual (sono, tolerância à cafeína), uso de linguagem exagerada ou sem base científica sólida.",
        "hint": "O corpo já produz hormônios de alerta ao acordar. Pense em como a cafeína interage com isso."
    },
    {
        "statement": "A foto de um presidente apertando a mão de um líder alienígena foi divulgada por um site de notícias satíricas e rapidamente se tornou viral nas redes sociais.",
        "image": "images/trump.jpg",
        "options": ["REAL", "FAKE"],
        "correct_answer": "FAKE",
        "explanation_what": "Imagens de líderes alienígenas são claramente obras de ficção ou sátira. A fonte foi explicitamente definida como 'site de notícias satíricas'.",
        "explanation_how": "Sempre verifique a fonte da notícia. Se for um site conhecido por humor ou sátira (ex: The Onion, Sensacionalista), o conteúdo é intencionalmente falso. Use a busca reversa de imagens para ver de onde a imagem realmente veio.",
        "explanation_red_flags": "Conteúdo bizarro ou inacreditável, fontes explicitamente satíricas, ausência de cobertura por veículos de imprensa confiáveis, indícios de manipulação digital (bordas estranhas, iluminação inconsistente).",
        "hint": "Sempre considere a fonte. Notícias muito bizarras podem ser sátira ou falsas."
    },
    {
        "statement": "Um artigo de um blog desconhecido alega que uma nova vacina contra o câncer foi desenvolvida, mas que as grandes farmacêuticas estão escondendo a cura.",
        "image": "images/vacina.jpeg",
        "options": ["REAL", "FAKE"],
        "correct_answer": "FAKE",
        "explanation_what": "Alegações de 'curas secretas' e 'conspirações' por grandes empresas são marcas registradas de fake news. Pesquisas médicas sérias são publicadas abertamente em periódicos científicos renomados e não em blogs anônimos.",
        "explanation_how": "Desconfie de narrativas que envolvem conspirações ou segredos. Informações sobre saúde devem vir de órgãos oficiais de saúde (OMS, Ministério da Saúde), universidades e periódicos científicos respeitados. Verifique se há validação por múltiplos estudos.",
        "explanation_red_flags": "Teorias da conspiração, acusações sem provas contra grandes instituições, fontes anônimas ou de reputação duvidosa, promessas de 'curas milagrosas' sem embasamento científico.",
        "hint": "Desconfie de teorias da conspiração e fontes não verificadas sobre curas milagrosas."
    },
    {
        "statement": "A agência espacial oficial (ex: NASA/ESA) publicou novas imagens de um planeta recém-descoberto, mostrando detalhes impressionantes da sua superfície e atmosfera.",
        "image": "images/planeta_cnn.jpeg",
        "options": ["REAL", "FAKE"],
        "correct_answer": "REAL",
        "explanation_what": "Agências espaciais oficiais têm como missão explorar o universo e divulgar suas descobertas ao público. É comum que publiquem imagens e dados de novas descobertas.",
        "explanation_how": "Sempre verifique a fonte oficial da agência (o site oficial, perfis de mídia social verificados). Procure por comunicados de imprensa, artigos científicos relacionados e a data da publicação para confirmar a autenticidade.",
        "explanation_red_flags": "Nenhum sinal de alerta aqui, pois a fonte é oficial e a notícia condiz com a atuação de uma agência espacial.",
        "hint": "Verifique se a fonte é uma organização oficial e confiável. Qual é o papel de agências espaciais?"
    },
    {
        "statement": "Um estudo científico recente publicado em uma revista de prestígio afirma que comer chocolate todos os dias prolonga a vida em 10 anos.",
        "image": "images/chocolate.jpeg",
        "options": ["REAL", "FAKE"],
        "correct_answer": "FAKE",
        "explanation_what": "A promessa de '10 anos a mais de vida' é exagerada e tipicamente não encontrada em pesquisas científicas sérias sobre alimentação. Estudos mostram benefícios moderados, não milagres.",
        "explanation_how": "Verifique a metodologia do estudo, a revista onde foi publicado (é revisada por pares?) e se a manchete é sensacionalista. Busque por consenso científico, não por um único estudo isolado.",
        "explanation_red_flags": "Exageros extremos ('milagre', 'cura', '10x melhor'), falta de citação de fontes renomadas, foco em um único alimento como solução para tudo.",
        "hint": "Promessas de benefícios extremos na saúde são frequentemente exageradas. Desconfie de 'milagres'."
    },
    {
        "statement": "Uma imagem de um 'novo animal' com cabeça de gato e corpo de pássaro foi viralizada, com muitos afirmando ser uma nova espécie descoberta na Amazônia, mas a imagem tem bordas pixelizadas e iluminação inconsistente.",
        "image": "images/animal.jpeg",
        "options": ["REAL", "FAKE"],
        "correct_answer": "FAKE",
        "explanation_what": "A combinação de características de animais diferentes (quimera) e falhas visuais como pixelização ou iluminação inconsistente são sinais clássicos de que a imagem foi gerada por IA ou manipulada digitalmente. IAs generativas ainda podem cometer erros sutis na representação da física do mundo.",
        "explanation_how": "Procure por anomalias visuais: sombras e reflexos que não batem, texturas estranhas, partes do corpo que não se conectam naturalmente, pixelização em áreas específicas. Use ferramentas de busca reversa de imagem. Desconfie de 'descobertas' extraordinárias sem validação científica.",
        "explanation_red_flags": "Combinações impossíveis na natureza, falhas na física (iluminação, sombras), geometria inconsistente, texturas 'borradas' ou pixelizadas em partes específicas da imagem, ausência de contexto ou fonte científica confiável.",
        "hint": "Observe a física da imagem e a consistência dos detalhes. Animais híbridos são comuns na natureza?"
    },
    {
        "statement": "Um vídeo de um famoso cientista fazendo uma palestra sobre física quântica parece ter coisas estranhas e com movimentos faciais ligeiramente artificiais.",
        "image": "images/palestra.jpeg",
        "options": ["REAL", "FAKE"],
        "correct_answer": "FAKE",
        "explanation_what": "Movimentos faciais artificiais, expressões irregulares 'robóticas' são sinais comuns de deepfakes de vídeo. A IA pode sobrepor um rosto em outro vídeo, mas ainda pode ter dificuldades em replicar a total naturalidade das microexpressões e movimentos corporais.",
        "explanation_how": "Observe os olhos (piscam demais ou de menos?), a boca (os movimentos labiais são sincronizados com a fala? a forma da boca é natural?), e o pescoço/mandíbula (há bordas estranhas?). Inconsistências na iluminação ou na qualidade da imagem entre o rosto e o corpo também são pistas.",
        "explanation_red_flags": "Sincronia labial imprecisa, movimentos dos olhos não naturais, falta de emoção ou expressões faciais 'mortas', iluminação inconsistente, desfoque ou pixelização em áreas críticas (rosto, bordas), ausência de vídeos originais ou fontes verificáveis.",
        "hint": "Piscadas e movimentos faciais antinaturais são frequentemente indicadores de manipulação em vídeos."
    }
]


# --- 2. Inicialização e Gestão do Estado da Sessão ---

def _init_session_state():

    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'start'
    if 'player_scores' not in st.session_state:
        st.session_state.player_scores = {"Jogador 1": 0, "Jogador 2": 0}
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'Jogador 1'
    if 'questions' not in st.session_state:
        st.session_state.questions = random.sample(QUESTIONS_DATA, len(QUESTIONS_DATA))
    if 'question_start_time' not in st.session_state:
        st.session_state.question_start_time = None
    if 'time_limit_per_question' not in st.session_state:
        st.session_state.time_limit_per_question = 15
    if 'answer_status' not in st.session_state:
        st.session_state.answer_status = None
    if 'selected_answer' not in st.session_state:
        st.session_state.selected_answer = None
    if 'show_hint_tooltip' not in st.session_state:
        st.session_state.show_hint_tooltip = False
    if 'explanation_display' not in st.session_state:
        st.session_state.explanation_display = None
    if 'result_title' not in st.session_state:
        st.session_state.result_title = None
    if 'result_message' not in st.session_state:
        st.session_state.result_message = None
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None


def _reset_question_state():
    st.session_state.answer_status = None
    st.session_state.selected_answer = None
    st.session_state.show_hint_tooltip = False
    st.session_state.explanation_display = None
    st.session_state.result_title = None
    st.session_state.result_message = None
    st.session_state.question_start_time = time.time()
    st.session_state.current_image = None


def _start_game():
    st.session_state.game_state = 'question'
    st.session_state.player_scores = {"Jogador 1": 0, "Jogador 2": 0}
    st.session_state.current_question_index = 0
    st.session_state.current_player = 'Jogador 1'
    st.session_state.questions = random.sample(QUESTIONS_DATA, len(QUESTIONS_DATA))
    _reset_question_state()


def _reset_game():
    st.session_state.game_state = 'start'
    st.session_state.player_scores = {"Jogador 1": 0, "Jogador 2": 0}
    st.session_state.current_question_index = 0
    st.session_state.current_player = 'Jogador 1'
    st.session_state.questions = random.sample(QUESTIONS_DATA, len(QUESTIONS_DATA))
    st.session_state.question_start_time = None
    _reset_question_state()


def _submit_answer(answer):
    if st.session_state.game_state != 'question' or st.session_state.answer_status is not None:
        return

    question = st.session_state.questions[st.session_state.current_question_index]
    correct_answer = question['correct_answer']
    is_timeout = answer == 'TIMEOUT'

    # Determina status e mensagem
    if is_timeout:
        st.session_state.answer_status = 'incorrect'
        st.session_state.result_title = 'Tempo esgotado!'
    elif answer == correct_answer:
        st.session_state.answer_status = 'correct'
        st.session_state.result_title = 'Correto!'
        st.session_state.result_message = 'Você acertou e ganhou 1 ponto.'
        st.session_state.player_scores[st.session_state.current_player] += 1
    else:
        st.session_state.answer_status = 'incorrect'
        st.session_state.result_title = 'Incorreto!'
    
    # Define mensagem da resposta correta se não foi acerto
    if st.session_state.answer_status == 'incorrect':
        st.session_state.result_message = f"A resposta correta era **{correct_answer}**."

    st.session_state.explanation_display = {
        'what': question['explanation_what'],
        'how': question['explanation_how'],
        'red_flags': question['explanation_red_flags'],
        'hint': question['hint'],
    }
    st.session_state.game_state = 'result'


def _next_question():
    next_index = st.session_state.current_question_index + 1
    if next_index >= len(st.session_state.questions):
        st.session_state.game_state = 'end'
        return

    st.session_state.current_question_index = next_index
    st.session_state.current_player = 'Jogador 1' if st.session_state.current_player == 'Jogador 2' else 'Jogador 2'
    _reset_question_state()
    st.session_state.game_state = 'question'


def _toggle_hint_tooltip():
    st.session_state.show_hint_tooltip = not st.session_state.show_hint_tooltip


# --- 3. UI e Renderização ---

def _display_start_screen():
    st.markdown('<div class="start-screen-box">', unsafe_allow_html=True)
    st.markdown('<h1 class="start-title">Detector de Fatos e Fakes (AI Edition)</h1>', unsafe_allow_html=True)
    st.markdown(
        "<div class='start-screen'><p class='start-description'>Bem-vindo ao game show interativo de detecção de desinformação. Avalie se cada afirmação é REAL ou FAKE e aprenda com explicações detalhadas ao final de cada rodada.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown('---')
    st.markdown('<div class="start-button-wrapper">', unsafe_allow_html=True)
    st.button('INICIAR JOGO', on_click=_start_game, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption('Cada pergunta tem um limite de tempo. Responda rápido e com atenção!')
    st.markdown('</div>', unsafe_allow_html=True)


def _display_question_screen():
    question = st.session_state.questions[st.session_state.current_question_index]

    if st.session_state.question_start_time is None:
        _reset_question_state()
    
    # Cacheia a imagem atual
    if st.session_state.current_image is None:
        st.session_state.current_image = question.get("image")

    elapsed = time.time() - st.session_state.question_start_time
    remaining = int(st.session_state.time_limit_per_question - elapsed)

    if remaining <= 0 and st.session_state.answer_status is None:
        _submit_answer('TIMEOUT')
        st.rerun()
        return

    player_class = 'player-turn player-1' if st.session_state.current_player == 'Jogador 1' else 'player-turn player-2'
    st.markdown(f"<div class='{player_class}'>Vez do <strong>{st.session_state.current_player}</strong></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-subtitle'>Pergunta {st.session_state.current_question_index + 1} de {len(st.session_state.questions)}</div>", unsafe_allow_html=True)

    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    col_left, col_right = st.columns([4, 1])
    with col_left:
        if remaining <= 5:
            st.markdown(f"<div class='timer timer-warning'>⏳ {remaining}s</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='timer'>⏳ {remaining}s</div>", unsafe_allow_html=True)
    with col_right:
        st.markdown('<div class="hint-button">', unsafe_allow_html=True)
        if st.button('Dica', key='hint_button'):
            _toggle_hint_tooltip()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="question-text">', unsafe_allow_html=True)
    st.write(question['statement'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Placeholder fixo para evitar conflito de DOM
    image_container = st.empty()
    
    if st.session_state.current_image:
        # Resolve o caminho corretamente
        image_path = st.session_state.current_image
        # Tenta encontrar o arquivo em relação ao diretório atual
        if not os.path.isabs(image_path) and not os.path.exists(image_path):
            # Se não existe, tenta no diretório do script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, image_path)
        
        if os.path.exists(image_path):
            with image_container:
                st.image(image_path, use_column_width=True)
        else:
            with image_container:
                st.markdown(
                    "<div style='margin-top:10px; color: gray; font-size:14px;'>⚠️ Imagem não encontrada</div>",
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.show_hint_tooltip:
        st.info('Dica: ' + question['hint'])

    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.markdown('<div class="real-button">', unsafe_allow_html=True)
        if st.button('É real', key='real_btn'):
            _submit_answer('REAL')
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col2:
        st.markdown('<div class="fake-button">', unsafe_allow_html=True)
        if st.button('É fake', key='fake_btn'):
            _submit_answer('FAKE')
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Timer atualiza automaticamente via autorefresh
    if st.session_state.answer_status is None:
        st_autorefresh(interval=1000, key=f"timer_{st.session_state.current_question_index}")


def _display_result_screen():
    status = st.session_state.answer_status
    title = st.session_state.result_title
    message = st.session_state.result_message

    if status == 'correct':
        st.success(title)
    elif status == 'incorrect':
        st.error(title)
    else:
        st.warning(title)

    st.markdown(f"<div class='result-message'>{message}</div>", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown('<h4>Explicação</h4>', unsafe_allow_html=True)
    st.markdown(f"<p><strong>O que aconteceu:</strong> {st.session_state.explanation_display['what']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Como identificar:</strong> {st.session_state.explanation_display['how']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Sinais de alerta:</strong> {st.session_state.explanation_display['red_flags']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Dica adicional:</strong> {st.session_state.explanation_display['hint']}</p>", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown('<h4>Pontuação Atual</h4>', unsafe_allow_html=True)
    score_col1, score_col2 = st.columns(2)
    with score_col1:
        st.metric('Jogador 1', st.session_state.player_scores['Jogador 1'])
    with score_col2:
        st.metric('Jogador 2', st.session_state.player_scores['Jogador 2'])

    st.write('')
    st.markdown('<div class="next-button">', unsafe_allow_html=True)
    if st.button('PRÓXIMA PERGUNTA'):
        _next_question()
    st.markdown('</div>', unsafe_allow_html=True)


def _display_end_screen():
    st.title('Fim do Game Show')
    st.subheader('Placar Final')

    sorted_scores = sorted(st.session_state.player_scores.items(), key=lambda item: item[1], reverse=True)
    for i, (player, score) in enumerate(sorted_scores, start=1):
        st.markdown(f"<p style='font-size:18px; margin: 0.2rem 0;'><strong>{i}. {player}</strong>: {score} pontos</p>", unsafe_allow_html=True)

    st.markdown('---')
    if len(sorted_scores) > 1 and sorted_scores[0][1] > sorted_scores[1][1]:
        st.success(f"{sorted_scores[0][0]} venceu! Excelente detecção de fake news.")
    else:
        st.info('Empate! Boa disputa entre os detetives.')

    st.write('')
    st.button('JOGAR NOVAMENTE', on_click=_reset_game, use_container_width=True)


# --- 4. Configuração da Página ---

st.set_page_config(layout='wide', page_title='Detector de Fatos e Fakes (AI Edition)', initial_sidebar_state='collapsed')

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700&display=swap');

    html, body, .stApp, .block-container {
        font-family: 'Inter', sans-serif;
        color: #1f2937;
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1000px;
        padding: 2rem 2rem 2.5rem 2rem;
    }

    .start-screen-box {
        max-width: 760px;
        margin: 4rem auto 2rem auto;
        padding: 2rem 2rem 2.25rem 2rem;
        background: #ffffff;
        border-radius: 28px;
        box-shadow: 0 24px 70px rgba(15, 23, 42, 0.08);
    }

    .start-screen {
        max-width: 760px;
        margin: 0 auto 1.25rem auto;
    }

    .start-title {
        text-align: center;
        margin: 0 auto 0.75rem auto;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.05;
        max-width: 720px;
    }

    .start-description {
        text-align: center;
        margin: 0 auto;
        max-width: 720px;
        font-size: 18px;
        color: #475569;
        line-height: 1.75;
    }

    .start-button-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 1.75rem;
        margin-bottom: 1rem;
    }

    .question-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: #4b5563;
        margin-bottom: 1rem;
        text-align: center;
    }

    .player-turn {
        font-family: 'Poppins', sans-serif;
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        padding: 1rem 1.25rem;
        border-radius: 20px;
        margin: 0 auto 1rem auto;
        max-width: 640px;
        line-height: 1.2;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
    }

    .player-turn.player-1 {
        background: #ecfdf5;
        color: #166534;
        border: 1px solid rgba(16, 185, 129, 0.18);
    }

    .player-turn.player-2 {
        background: #fef2f2;
        color: #991b1b;
        border: 1px solid rgba(239, 68, 68, 0.18);
    }

    .question-card {
        padding: 1.5rem 1.5rem 1.25rem;
        border-radius: 24px;
        background: #ffffff;
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.06);
        margin-bottom: 1.6rem;
    }

    .button-row {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .question-subtitle, .timer, .question-text {
        font-family: 'Inter', sans-serif;
    }

    .timer {
        font-size: 18px;
        font-weight: 700;
        color: #1f2937;
        padding: 0.85rem 1rem;
        background: #e2e8f0;
        border-radius: 14px;
        display: inline-block;
    }

    .timer-warning {
        background: #fde2e2;
        color: #b91c1c;
    }

    .question-text {
        font-size: 18px;
        line-height: 1.75;
        color: #111827;
        margin-bottom: 1.1rem;
    }

    .result-message {
        font-size: 16px;
        margin-bottom: 1rem;
        color: #334155;
    }

    .stButton>button {
        border-radius: 14px !important;
        padding: 10px 16px !important;
        font-size: 15px !important;
        min-width: 150px !important;
        max-width: 220px !important;
        width: auto !important;
    }

    .real-button button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
    }

    .fake-button button {
        background-color: #F44336 !important;
        color: white !important;
        border: none !important;
    }

    .hint-button button {
        background-color: #F5DEB3 !important;
        color: #111827 !important;
        border: none !important;
    }

    .next-button button {
        background-color: #4A90E2 !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

_init_session_state()

if st.session_state.game_state == 'start':
    _display_start_screen()
elif st.session_state.game_state == 'question':
    _display_question_screen()
elif st.session_state.game_state == 'result':
    _display_result_screen()
elif st.session_state.game_state == 'end':
    _display_end_screen()
