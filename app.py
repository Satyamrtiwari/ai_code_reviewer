import streamlit as st
from graph.workflow import create_workflow

st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")

# Side bar for file upload and stuff
with st.sidebar:
    st.header("📂 Upload Your Code")
    uploaded_file = st.file_uploader("Pick a file", type=["py", "js", "java", "c", "cpp"])
    
    # helper for mapping exts to langs
    ext_map = {
        "py": "Python",
        "js": "JavaScript",
        "java": "Java",
        "c": "C",
        "cpp": "C++"
    }
    
    default_lang = "Python"
    default_code = ""
    
    if uploaded_file is not None:
        # readin the file
        default_code = uploaded_file.getvalue().decode("utf-8")
        # detect what lang it is
        ext = uploaded_file.name.split(".")[-1].lower()
        default_lang = ext_map.get(ext, "Python")
        st.success(f"Loaded: {uploaded_file.name}")

st.title("🤖 AI Code Reviewer")
st.markdown("An intelligent code review assistant powered by Python, LangGraph, AST, LLM")

col1, col2 = st.columns([3, 1])
with col1:
    # use state if we uploaded sumthin
    code_input = st.text_area("Paste your code here:", height=300, 
                              value=default_code,
                              placeholder="def hello_world():\n    print('Hello World!')")
with col2:
    # find the index for the dropdown
    lang_options = ["Python", "JavaScript", "Java", "C", "C++"]
    try:
        lang_index = lang_options.index(default_lang)
    except ValueError:
        lang_index = 0
        
    language = st.selectbox("Language", lang_options, index=lang_index)

if st.button("Review My Code", type="primary"):
    if not code_input.strip():
        st.warning("Please enter some code to review.")
    else:
        with st.spinner("Agents are reviewing your code..."):
            try:
                app = create_workflow()
                initial_state = {"code": code_input, "language": language}
                
                # Run the graph
                final_state = app.invoke(initial_state)
                
                ast_analysis = final_state.get("ast_analysis", {})
                bugs = final_state.get("bugs", [])
                quality = final_state.get("quality_review", {})
                rewritten_code = final_state.get("rewritten_code", "")
                
                st.success("All Done!")
                
                # Show results here
                with st.expander("📊 Overview & Score", expanded=True):
                    score = quality.get("score", 0)
                    col_metric, col_summary = st.columns([1, 3])
                    with col_metric:
                        st.metric(label="Quality Score", value=f"{score}/100")
                    with col_summary:
                        num_lines = ast_analysis.get('num_lines', 0)
                        
                        if language == "Python":
                            num_classes = len(ast_analysis.get('class_names', []))
                            num_funcs = len(ast_analysis.get('function_names', []))
                            st.write(f"**Lines:** {num_lines} | **Classes:** {num_classes} | **Funcs:** {num_funcs}")
                        else:
                            st.write(f"**Lines of Code:** {num_lines} | **Language:** {language}")
                        
                        if score >= 90:
                            st.write("Overall, the code quality is excellent, with minimal issues.")
                        elif score >= 70:
                            st.write("The code is structurally sound but has several areas for improvement.")
                        else:
                            st.write("The code requires significant refactoring to meet production standards.")
                            
                        issues = ast_analysis.get("issues", [])
                        if issues:
                            st.write("**Structural Warnings:**")
                            for issue in issues:
                                st.write(f"- ⚠️ {issue}")

                # 2. Bug Report
                with st.expander("🐛 Bug Report", expanded=True):
                    if not bugs:
                        st.write("✅ No bugs detected!")
                    else:
                        for bug in bugs:
                            severity = bug.get('severity', 'LOW').upper()
                            line = bug.get('line_number', 'N/A')
                            issue_desc = bug.get('issue', 'Unknown issue')
                            
                            if severity == "HIGH":
                                st.error(f"**[{severity}] Line {line}:** {issue_desc}", icon="🔴")
                            elif severity == "MEDIUM":
                                st.warning(f"**[{severity}] Line {line}:** {issue_desc}", icon="🟠")
                            else:
                                st.info(f"**[{severity}] Line {line}:** {issue_desc}", icon="🟡")

                # 3. Improvement Suggestions
                with st.expander("💡 Improvement Suggestions", expanded=True):
                    suggestions = quality.get("suggestions", [])
                    if not suggestions:
                        st.write("✅ No further suggestions.")
                    else:
                        for i, suggestion in enumerate(suggestions[:5], 1): # Top 5 only
                            st.markdown(f"**{i}.** {suggestion}")

                # 4. Rewrite Full Code Correctly
                with st.expander("✨ Rewrite Full Code Correctly", expanded=True):
                    if not rewritten_code or rewritten_code.startswith("# Error"):
                        st.warning("Could not rewrite the code. Check the error above.")
                    else:
                        st.code(rewritten_code, language=language.lower() if language != "C++" else "cpp")
                        st.download_button(
                            label="⬇️ Download Rewritten Code",
                            data=rewritten_code,
                            file_name=f"rewritten_code.{language.lower()}",
                            mime="text/plain"
                        )
                
            except Exception as e:
                st.error(f"An error occurred during review: {str(e)}")

