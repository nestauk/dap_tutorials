# **Streamlit**

Streamlit is an [open-source python framework](streamlit.io) for building web apps for Machine Learning and Data Science.

It's a powerful tool to simply create web apps which can have a range of functionalities. The best way to see what Streamlit can do is to explore the [gallery](https://streamlit.io/gallery) as you can explore different web apps in action and also view the app source code to see how each feature was created.

## **Quick summary of Streamlit's features**
There is a handy [cheat sheet](https://docs.streamlit.io/library/cheatsheet) online which summarises a lot of the code you will need, but here are some of the features which are most useful to get you started:
- Inserting [interactive and static graphs](https://docs.streamlit.io/library/api-reference/charts)
    - You can easily add in `altair`, `bokeh`, `plotly`, `pydeck` and `matplotlib` plots as well as Streamlit's in-built graphing functions.
    - This includes maps from `folium` and `deck.gl`.
- Inserting both [static and interactive tables either directly from `pandas` or other libraries (e.g. `plotly`) as well as having large metrics printed](https://docs.streamlit.io/library/api-reference/data).
- [User selections](https://docs.streamlit.io/library/api-reference/widgets) such as radio buttons, uploading/downloading data, camera input, text input
- [Adding passwords (and usernames) to apps to protect them](https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso)
- [Multi-page apps](https://blog.streamlit.io/introducing-multipage-apps/)
- Easily add in [images, videos and audio](https://docs.streamlit.io/library/api-reference/media).
- Lots of flexibility with the blocks of text, you can add in [text with variables that can be changed by other user selections, LaTeX, code blocks](https://docs.streamlit.io/library/api-reference/text).
- You can change the font and theme of the Streamlit app with an overall [theme config](https://docs.streamlit.io/library/advanced-features/theming).

### **Other useful features**
- [You can add in progress measures when loading](https://docs.streamlit.io/library/api-reference/status) - you can even have [celebratory balloons](https://docs.streamlit.io/library/api-reference/status/st.balloons)!
- [You can be very specific in the layout with containers](https://docs.streamlit.io/library/api-reference/layout).


## **Instructions for the have-a-go**

For the have-a-go, we're just going to edit the existing app and you can try adding in tables, new user selections or new graphs as this is the easiest way to learn Streamlit.

If you're not feeling the rugby theme, have a look at the [Streamlit gallery](https://streamlit.io/gallery) and you can copy one of their apps (just click `view app source code`) and try and edit that.

### **Steps**


1. `git clone git@github.com:nestauk/dap_tutorials.git`
2. `cd dap_tutorials/streamlit_demo`
3. `conda create --name streamlit_demo python`
4. `conda activate streamlit_demo`
5. `pip install -r requirements.txt`

**Now we need to add in the secrets file so the password will work.**

6. `mkdir .streamlit && touch secrets.toml`


7. In the `.streamlit/secrets.toml` file create a password so the file should look like this:
```
PASSWORD = "streamlitdemo"
```
8. We can now run the app `streamlit run streamlit_six_nations_demo.py`


It should automatically open in a web browser, if not, just copy and paste the link across.

You can edit the source code (`streamlit_six_nations_demo.py`) in your favourite Python editor, and when you save it, it should automatically prompt you to rerun the Streamlit app on the web page.

**Hope you all enjoy and have fun getting creative with Streamlit!!** :tada:
