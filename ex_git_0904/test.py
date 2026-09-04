import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "민원인", "회신인", "관리자"]

def login():
    st.header("로그인")
    role = st.selectbox("선생님의 직업을 골라주세요", ROLES)

    if st.button("로그인"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

logout_page = st.Page(
    logout,
    title="로그아웃",
    icon=":material/logout:"
)

settings = st.Page(
    "settings.py",
    title="설정",
    icon=":material/settings:"
)

request_1 = st.Page(
    "request/request_1.py",
    title="민원인 1",
    icon=":material/help:",
    default=(role == "민원인"),
)

request_2 = st.Page(
    "request/request_2.py",
    title="민원인 2",
    icon=":material/bug_report:"
)

respond_1 = st.Page(
    "respond/respond_1.py",
    title="회신인 1",
    icon=":material/healing:",
    default=(role == "회신인"),
)

respond_2 = st.Page(
    "respond/respond_2.py",
    title="회신인 2",
    icon=":material/handyman:"
)

admin_1 = st.Page(
    "admin/admin_1.py",
    title="관리자 1",
    icon=":material/person_add:",
    default=(role == "관리자"),
)

admin_2 = st.Page(
    "admin/admin_2.py",
    title="관리자 2",
    icon=":material/security:"
)

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("민원인 매니저")
st.logo(
    "images/horizontal_blue.png",
    icon_image="images/icon_blue.png"
)

page_dict = {}

if st.session_state.role in ["민원인", "관리자"]:
    page_dict["Request"] = request_pages

if st.session_state.role in ["회신인", "관리자"] :
    page_dict["Respond"] = respond_pages

if st.session_state.role == "관리자":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0: 
    pg = st.navigation(
        {"Account": account_pages} | page_dict
    )
else:
    pg = st.navigation(
        [st.Page(login)]
    )
pg.run()