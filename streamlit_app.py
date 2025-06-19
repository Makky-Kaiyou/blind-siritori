import streamlit as st
import re
import random

# プレイヤー名
p1 = "プレイヤー1"
p2 = "プレイヤー2"

# セッション状態初期化
if 'p1_words' not in st.session_state:
    st.session_state.p1_words = []
if 'p2_words' not in st.session_state:
    st.session_state.p2_words = []
if 'turn' not in st.session_state:
    st.session_state.turn = 1
if 'last_char' not in st.session_state:
    st.session_state.last_char = ""
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# ひらがな判定
def is_hiragana(text):
    return bool(re.fullmatch(r'[ぁ-んー]+', text))

# ランダムな最初の文字を生成（"ん"と"を"を除外）
def generate_initial_char():
    chars = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわ")
    return random.choice(chars)

# タイトル
st.title("ブラインドしりとり（２人用）")

# ▶️ ゲーム開始前：ルール説明とボタン
if not st.session_state.game_started:
    st.markdown("### 〈ルール説明〉")
    st.markdown("""
- このゲームは２人用です。  
- 基本的なルールは一般的なしりとりと同じですが、異なる点がいくつかあります。  
- 単語の入力はすべて **ひらがな** で行ってください。  

1. 「ゲームを開始する」を押した後、**最初の文字が指定**されます。両プレイヤーはその文字を確認してください。  
2. 自分の番のプレイヤーは、**指定された文字から始まる単語**を入力してください。  
　　- 相手プレイヤーが単語を入力している間は、**画面を見ない**ようにしてください。  
　　- 相手が入力した単語の**最後の文字が表示**されるので、**相手が入力した単語を推測**し、それ避けながら単語を考えてください。  

- 一般的なしりとりと同様、**すでに使った単語**や「**ん**」で終わる単語を入力すると負けになります。  
- ゲーム終了後、入力された単語の**履歴が表示**されるので、「えっぅぃあ」など**存在しない単語**で不正をしていないか確認しましょう。  
　　不正が発覚した場合、より早く**不正をしたプレイヤーが負け**になります。  
　　不正かどうかは、両プレイヤー間で話し合って決めてください。  
　　不正がなかった場合は、**そのまま決着が有効**となります。
    """)

    if st.button("▶️ ゲームを開始する"):
        st.session_state.last_char = generate_initial_char()
        st.session_state.game_started = True
        st.rerun()
    else:
        st.stop()

# 現在のプレイヤー
current_player = p1 if st.session_state.turn == 1 else p2
word_key = f"word_input_{st.session_state.turn}"

if not st.session_state.game_over:
    st.subheader(f" {current_player} の番です")

    # 🔄 最初のターンだけ「最初の文字は」表示、それ以降は「最後の文字は」
    if not st.session_state.p1_words and not st.session_state.p2_words:
        st.markdown(f"**最初の文字は「{st.session_state.last_char}」です**")
    else:
        st.markdown(f"**最後の文字は「{st.session_state.last_char}」です**")

    word = st.text_input("ひらがなで単語を入力してください", key=word_key)

    if st.button("この単語で決定"):
        used_words = st.session_state.p1_words + st.session_state.p2_words

        if not word:
            st.warning("単語を入力してください")
        elif not is_hiragana(word):
            st.error("🚫 ひらがなのみ使用可能です")
        elif not used_words and word[0] != st.session_state.last_char:
            st.error(f"最初の単語は「{st.session_state.last_char}」で始めてください！")
        elif used_words and word[0] != st.session_state.last_char:
            st.error(f"❌ 単語は「{st.session_state.last_char}」から始めてください！")
            winner = p2 if current_player == p1 else p1
            st.session_state.game_over = True
            st.markdown(f"🎉 **{winner} の勝ち！**")
        elif word in used_words:
            st.error("🚫 すでに使われた単語です")
            winner = p2 if current_player == p1 else p1
            st.session_state.game_over = True
            st.markdown(f"🎉 **{winner} の勝ち！**")
        elif word[-1] == "ん":
            st.error("✖「ん」で終わる単語は負けです！")
            winner = p2 if current_player == p1 else p1
            st.session_state.game_over = True
            st.markdown(f"🎉　**{winner} の勝ち！**")
        else:
            if st.session_state.turn == 1:
                st.session_state.p1_words.append(word)
                st.session_state.turn = 2
            else:
                st.session_state.p2_words.append(word)
                st.session_state.turn = 1
            st.session_state.last_char = word[-1]
            st.rerun()

# ゲーム終了後：履歴表示＆再挑戦ボタン
if st.session_state.game_over:
    st.markdown("### 使用単語履歴")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{p1} が使った単語**")
        for i, w in enumerate(st.session_state.p1_words, 1):
            st.markdown(f"{i}. {w}")
    with col2:
        st.markdown(f"**{p2} が使った単語**")
        for i, w in enumerate(st.session_state.p2_words, 1):
            st.markdown(f"{i}. {w}")

    if st.button("🔁 もう一度プレイ"):
        st.session_state.p1_words = []
        st.session_state.p2_words = []
        st.session_state.turn = 1
        st.session_state.last_char = ""
        st.session_state.game_over = False
        st.session_state.game_started = False
        st.rerun()
