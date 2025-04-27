import streamlit as st

def render_wizard_progress(current_step=1, total_steps=4, step_titles=None):
    """
    Render a progress bar for wizards with multiple steps
    
    Parameters:
    ----------
    current_step : int
        Current step number (1-based index)
    total_steps : int
        Total number of steps
    step_titles : list
        List of titles for each step
    """
    if step_titles is None:
        step_titles = [f"Step {i}" for i in range(1, total_steps + 1)]
    
    # Create columns for each step
    cols = st.columns(total_steps)
    
    for i, col in enumerate(cols, 1):
        # Determine step class based on current step
        step_class = ""
        if i < current_step:
            step_class = "step-completed"
        elif i == current_step:
            step_class = "step-active"
        
        # Render the step in the appropriate column
        col.markdown(f'''
        <div class="progress-step {step_class}">
            <div class="step-number">{i}</div>
            <div class="step-text">{step_titles[i-1]}</div>
        </div>
        ''', unsafe_allow_html=True)

def render_wizard_nav_buttons(back_callback=None, next_callback=None, current_step=1, total_steps=4, 
                             next_text="Lanjut", back_text="Kembali", finish_text="Selesai"):
    """
    Render navigation buttons for wizard
    
    Parameters:
    ----------
    back_callback : function
        Function to call when back button is clicked
    next_callback : function
        Function to call when next button is clicked
    current_step : int
        Current step number
    total_steps : int
        Total number of steps
    next_text : str
        Text for next button
    back_text : str
        Text for back button
    finish_text : str
        Text for finish button (on last step)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        if current_step > 1 and back_callback:
            if st.button(f"⬅ {back_text}", key="back_btn", use_container_width=True):
                back_callback()
    
    with col2:
        if current_step < total_steps and next_callback:
            if st.button(f"{next_text} ➡", key="next_btn", use_container_width=True):
                next_callback()
        elif current_step == total_steps and next_callback:
            if st.button(f"✅ {finish_text}", key="finish_btn", use_container_width=True):
                next_callback()