import os
import streamlit as st
import streamlit_authenticator as stauth
import webui
import yaml
from yaml.loader import SafeLoader
import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address

api = ApiRequest(base_url=api_address())
st.set_page_config(
    "华测检测 CTI-AI",
    os.path.join("img", "chatchat_icon_blue_square_v2.png"),
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': 'mailto:aaron.zhu@cti-cert.com'
    }
)  

with open('auth.yaml','rb') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('登录', 'main')

if authentication_status: 
    st.sidebar.image(
            os.path.join(
                "img",
                "logo-long-chatchat-trans-v2.png"
            ),
            use_column_width=True
        )
    st.sidebar.info('欢迎 *%s*' % (name))
    authenticator.logout('退出登录', 'sidebar')      

    pages = {
            "对话": {
                "icon": "chat",
                "func": dialogue_page,
            }
        }    
    #admin才有知识管理
    if username == 'admin':
        pages['知识库管理'] = {   
        "icon": "hdd-stack",
        "func": knowledge_base_page,
        }

    with st.sidebar:     
        options = list(pages)
        icons = [x["icon"] for x in pages.values()]

        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,
        )

    if selected_page in pages:
        pages[selected_page]["func"](api)

    if not chat_box.chat_inited:
        st.toast(
            f"欢迎使用 [`CTI-AI`](https://www.cti-cert.com/) ! \n\n"
            f"当前使用模型`{llm_model_dict[LLM_MODEL]['name']}`, 您可以开始提问了."
        )

elif authentication_status == False:
    st.error('用户名或密码错误')
elif authentication_status == None:
    st.warning('请输入用户名和密码')  

try:
    if authenticator.register_user('Register user', preauthorization=False):
        with open('../config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        st.success('User registered successfully')
except Exception as e:
    st.error(e)

st.markdown('''<style>
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-2zqmbv.eczjsme11 > div.css-6qob1r.eczjsme3 > div.css-10oheav.eczjsme4 {
    padding: 1rem 1rem;
            }
}
</style>''', unsafe_allow_html=True)