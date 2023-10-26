import datetime
import os
import streamlit as st
import streamlit_authenticator as stauth
from configs.model_config import ONLINE_LLM_MODEL
import yaml
from yaml.loader import SafeLoader
import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address
import streamlit.components.v1 as components


api = ApiRequest(base_url=api_address())
st.set_page_config(
    "华测检测 CTI-AI",
    os.path.join("img", "chatchat_icon_blue_square_v2.png"),
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': 'mailto:aaron.zhu@cti-cert.com'
    },
    # layout="wide"
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

# name, authentication_status, username = authenticator.login('登录', 'main')

source = authenticator.cookie_manager.get('source')

def home(login_username,login_name):
    st.sidebar.image(
            os.path.join(
                "img",
                "logo-long-chatchat-trans-v2.png"
            ),
            use_column_width=True
        )
    if login_username == 'admin':
        st.sidebar.info('欢迎 *%s*' % (login_name))
        authenticator.logout('退出登录', 'sidebar')      

    pages = {
            "对话": {
                "icon": "chat",
                "func": dialogue_page,
            }
        }    
    #admin才有知识管理
    if login_username == "admin":
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
            f"当前使用模型`{ONLINE_LLM_MODEL[LLM_MODEL]['name']}`, 您可以开始提问了."
        )


if source == 'wxwork':
    home("guest","")
else:
    name, authentication_status, username = authenticator.login('登录', 'main')
    if authentication_status: 
        print('login')
        home(username,name)
    elif authentication_status == False:
        st.error('用户名或密码错误')
    elif authentication_status == None:
        st.warning('请输入用户名和密码')  
# #注册
# try:
#     if authenticator.register_user('Register user', preauthorization=False):
#         with open('../config.yaml', 'w') as file:
#             yaml.dump(config, file, default_flow_style=False)
#         st.success('User registered successfully')
# except Exception as e:
#     st.error(e)


st.markdown('''<style>
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-2zqmbv.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-10oheav.eczjsme4 {
    padding: 2rem 1rem;
            }
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.ea3mdgi5 > div.block-container.css-1y4p8pa.ea3mdgi4{
    padding: 1rem 1rem 10rem;
            }
</style>''', unsafe_allow_html=True)

js_code = '''    
        var ua = navigator.userAgent.toLowerCase(); // 将用户代理头的值转为小写
        if(ua.match(/wxwork/i) == 'wxwork')
        {
            console.log("企业微信浏览器环境下")
            var now=new Date();
            //设置过期时间
            now.setMinutes(now.getMinutes()+5)
            //设置Cookie
            document.cookie='source=wxwork;expires='+now.toUTCString()
        }else{
            console.log("非企业微信环境")
            document.cookie='source=0'
        }
        console.log(ww.SDK_VERSION)
        
'''
components.html(f''' 
    <script src="https://wwcdn.weixin.qq.com/node/open/js/wecom-jssdk-1.3.1.js"></script>
    <script>{js_code}</script>
    ''',
     height=0)