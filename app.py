import json
import random

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from st_login import Login

with open("./data.json", "r", encoding="utf8") as f:
    data = json.loads(f.read())


class CustomPage(Login):
    def nav_sidebar(self):
        """
        Creates the side navigaton bar
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title='用户信息',
                menu_icon='list-columns-reverse',
                icons=['box-arrow-in-right', 'person-plus', 'x-circle', 'arrow-counterclockwise'],
                options=['Login', 'Create Account', 'Forgot Password?', 'Reset Password'],
                styles={
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"}})
        return main_page_sidebar, selected_option

    def logout_widget(self) -> None:
        """
        Creates the logout widget in the sidebar only if the user is logged in.
        """
        if st.session_state['LOGGED_IN'] == True:
            self.sidebar_after_login()
            self.main_page_after_login()

    def logout_button(self):
        logout_click_check = st.button(self.logout_button_name)
        st.sidebar.empty()
        if logout_click_check == True:
            st.session_state['LOGOUT_BUTTON_HIT'] = True
            st.session_state['LOGGED_IN'] = False
            self.cookies['__streamlit_login_signup_ui_username__'] = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
            st.empty()
            st.experimental_rerun()

    def sidebar_after_login(self):
        st.sidebar.empty()
        with st.sidebar:
            st.markdown("# AI")

            is_need_login = st.selectbox(label="是否需要登录", options=["", '是', '否'])
            media_type = st.selectbox(label="应用类型", options=["", '文本类', '图像类', "视频类"])
            is_need_vpn = st.selectbox(label="是否需要vpn", options=["", '是', '否'])
            is_free = st.selectbox(label="是否免费", options=["", '是', '否'])

            st.session_state['is_need_login'] = is_need_login
            st.session_state['media_type'] = media_type
            st.session_state['is_need_vpn'] = is_need_vpn
            st.session_state['is_free'] = is_free
            self.logout_button()
            # reset_click = st.button("重置查询条件")
            # if reset_click == True:
            #     st.empty()
            #     st.experimental_rerun()

    def main_page_after_login(self):
        """
        {
            "image": "https://lijiacai-chatgpt-next-web.hf.space/favicon.ico",
            "name": "test",
            "url": "https://lijiacai-ai-set.hf.space/",
            "is_need_login": "否",
            "media_type": "文本类",
            "is_need_vpn": "否",
            "is_free": "是",
            "author": "黎家才"
          },
        :return:
        """

        def add_condition(df_: pd.DataFrame, key):
            value = st.session_state[key]
            if value:
                df_ = df_[df_[key] == value]
            return df_

        df = pd.DataFrame(data=data)
        df = add_condition(df, key="is_need_login")
        df = add_condition(df, key="media_type")
        df = add_condition(df, key="is_need_vpn")
        df = add_condition(df, key="is_free")
        with st.container():
            st.dataframe(
                df,
                column_config={
                    "image": st.column_config.ImageColumn("图标"),
                    "name": "应用名称",
                    "url": st.column_config.LinkColumn("访问地址"),
                    "is_need_login": st.column_config.TextColumn("是否需要登录"),
                    "media_type": st.column_config.TextColumn("应用类型"),
                    "is_need_vpn": st.column_config.TextColumn("是否需要vpn"),
                    "is_free": st.column_config.TextColumn("是否免费"),
                    "author": st.column_config.TextColumn("作者"),
                    "desc": st.column_config.TextColumn("说明")
                },
                # hide_index=True,
                width=1400,
                # height=500
            )


st.set_page_config(layout="wide")
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('client.showErrorDetails', False)

CustomPage(auth_token="courier_auth_token",
           company_name="Shims",
           width=200, height=250,
           logout_button_name='退出登录', hide_menu_bool=True,
           hide_footer_bool=False,
           lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json').build_login_ui()
