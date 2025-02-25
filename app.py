import streamlit as st
import pickle
import pandas as pd
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="SMA Gene Therapy Survey",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_welcome_screen():
    # Welcome screen container with styling
    welcome_container = st.container()
    with welcome_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://cdn.capsulcn.com/Content/Images/uploaded/ZOLGENSMA_logo.png", width=200)
            st.title("Welcome to the Zolgensma HCP Typing Tool")
            
            st.markdown("""
            ### Purpose of this Tool
            
            This survey helps categorize healthcare professionals (HCPs) based on their attitudes and practices 
            regarding gene therapy prescribing for SMA patients.
            
            ### How to Use
            
            1. Complete the survey with information about the HCP
            2. Submit the form to receive the HCP categorization
            3. View detailed scores and recommendations based on the profile
            
            ### HCP Categories
            
            - **GTx Champions**: Early adopters who are confident in prescribing gene therapies
            - **Risk Balancers**: Cautious adopters with concerns about safety profiles
            - **RWE Seekers**: HCPs who seek real-world evidence before adoption
            
            ### Data Privacy
            
            All submitted information is kept confidential and used only for HCP categorization purposes.
            """)
            
            # Continue button centered
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            if st.button("Continue to Survey", key="welcome_continue"):
                st.session_state.show_welcome = False  # Proceed with the transition on the first click
            st.markdown("</div>", unsafe_allow_html=True)


def main(model_data):
    # Check if we need to show the welcome screen
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
        show_welcome_screen()
    else:
        # Sidebar for information
        with st.sidebar:
            st.image("https://cdn.capsulcn.com/Content/Images/uploaded/ZOLGENSMA_logo.png", width=150)
            st.markdown("### About This Survey")
            st.markdown("This tool collects data about gene therapy prescribing practices for SMA patients and provides insights into prescriber categorization.")
            
            st.markdown("### HCP Categories")
            st.markdown("**GTx Champions**: Early adopters of gene therapies who are confident in prescribing them.")
            st.markdown("**Risk Balancers**: Cautious in adopting new therapies with concerns about safety.")
            st.markdown("**RWE Seekers**: Interested in real-world evidence before adopting new therapies.")
            # have cards for each hcp categories

            st.markdown("---")
            st.markdown(f"Survey Date: {datetime.now().strftime('%B %d, %Y')}")
        
        # Main content
        st.title("Zolgensma HCP Typing Tool")
        st.markdown("Please complete the following survey to determine the attitudinal segments for an HCP.")
        
        # Create two columns for the initial inputs
        col1, col2 = st.columns(2)
        with col1:
            npi_id = st.text_input("NPI ID", placeholder="Enter NPI ID")
        with col2:
            reps_name = st.text_input("HCP Name", placeholder="Enter representative's name")
        
        # Create a form for the survey
        with st.form("survey_form"):
            # Question 1 - Checkboxes
            st.header("Q1: Primary Rationale for Switching to Gene Therapies")
            st.markdown("Please select the primary rationale for considering switching to gene therapies  \n (Select all relevent options):")
            
            col1, col2 = st.columns(2)
            with col1:
                q1_efficacy = st.checkbox("Efficacy", help="Select if efficacy is a primary rationale")
                q1_safety = st.checkbox("Safety", help="Select if safety is a primary rationale")
            with col2:
                q1_moa = st.checkbox("MOA (Mechanism of Action)", help="Select if mechanism of action is a primary rationale")
                q1_dosing = st.checkbox("Dosing Convenience", help="Select if dosing convenience is a primary rationale")
            
            st.markdown("---")
            
            # Question 2 - Radio button
            st.header("Q2: Confidence in Prescribing")
            st.markdown("Please select to what extent the HCP is confident in prescribing gene therapy for SMA patients for 1L treatment:")
            # q2_options = ["Extremely Confident", "Slightly Confident", "Not Confident at All"]
            q2_options = ["Select an option", "Extremely Confident", "Slightly Confident", "Not Confident at All"]
            q2_answer = st.radio(
                "Confidence Level",
                options=q2_options,
                horizontal=True,
                key="q2_radio",
                index= 0
            )
            
            st.markdown("---")
            
            # Question 3 - Radio button
            st.header("Q3: Institutional Influence")
            st.markdown("Please indicate to what extent this HCP's institution influences their decision to adopt new therapies like Zolgensma:")
            # q3_options = ["Extremely Influential", "Slightly Influential", "Not at all"]
            q3_options = ["Select an option", "Extremely Influential", "Slightly Influential", "Not at all"]
            q3_answer = st.radio(
                "Influence Level",
                options=q3_options,
                horizontal=True,
                key="q3_radio"
            )
            
            st.markdown("---")
            
            # Question 4 - Radio button
            st.header("Q4: Satisfaction with Current Standard of Care")
            st.markdown("Please select the extent of satisfaction the HCP has with the current standard of care therapies for SMA:")
            # q4_options = ["Extremely Satisfied", "Neutral", "Dissatisfied"]
            q4_options = ["Select an option", "Extremely Satisfied", "Neutral", "Dissatisfied"]
            q4_answer = st.radio(
                "Satisfaction Level",
                options=q4_options,
                horizontal=True,
                key="q4_radio",
                index= 0
            )
            
            st.markdown("---")
            
            # Question 5 - Radio button
            st.header("Q5: Key Barriers")
            st.markdown("Please select what are the key barriers for HCPs in prescribing gene therapies:")
            # q5_options = [
            #     "Lack of experience prescribing Zolgensma",
            #     "Institutional barrier - Lack of GTx capabilities at site",
            #     "Lack of MDT support at the institute",
            #     "None of the Above"
            # ]
            q5_options = [ 
                "Select an option", 
                "Lack of experience prescribing Zolgensma", 
                "Institutional barrier - Lack of GTx capabilities at site", 
                "Lack of MDT support at the institute", 
                "None of the Above"
            ]
            q5_answer = st.radio(
                "Key Barrier",
                options=q5_options,
                key="q5_radio",
                index= 0
            )
            
            st.markdown("---")
            
            # Question 6 - Radio button
            st.header("Q6: Patient Referral(Optional)")
            st.markdown("Do you expect that you would need to refer your patients to receive treatment with Gene Therapy?")
            # q6_options = [
            #     "I do not need to refer my patients", 
            #     "I may need to refer my patients to a colleague at my institution", 
            #     "I may need to refer my patients to another institution"
            # ]
            q6_options = [
                "Select an option",
                "I do not need to refer my patients",
                "I may need to refer my patients to a colleague at my institution",
                "I may need to refer my patients to another institution"
            ]
            q6_answer = st.radio(
                "Referral Needs",
                options=q6_options,
                key="q6_radio",
                index= 0
            )
            
            # Submit button with standard styling
            submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
            with submit_col2:
                submit_button = st.form_submit_button("Submit Survey")
            
            
        
    

        # Handle form submission
        if submit_button:
            if not npi_id or not reps_name or q2_answer == "Select an option" or q3_answer == "Select an option" or q4_answer == "Select an option" or q5_answer == "Select an option" or q6_answer == "Select an option":
                st.error("Please select an option for all questions before submitting.")
            else:
                # Create mixed response array
                response_array = []
                response_array.append(q2_answer)  # Q2
                response_array.append(q4_answer)  # Q4
                response_array.append(q5_answer)  # Q5

                # Q1: Convert checkboxes to binary values (1 if selected, 0 if not)
                response_array.append(1 if q1_efficacy else 0)
                response_array.append(1 if q1_safety else 0)
                response_array.append(1 if q1_moa else 0)
                response_array.append(1 if q1_dosing else 0)
                
                # Add actual text selections for all other questions
                response_array.append(q3_answer)  # Q3
                # Q6 is not used in the model but saved in the response file
                
                # Load model components
                loaded_model = model_data['model']
                loaded_label_encoder = model_data['label_encoder']
                onehot = model_data['one_hot_encoder']

                # Create a DataFrame from the response array
                response_df = pd.DataFrame([response_array], columns=model_data['questions'])
                
                # Transform the data for prediction
                response_hot = onehot.transform(response_df).toarray()
                
                # Make predictions
                prediction = loaded_model.predict(response_hot)
                prediction_score = loaded_model.predict_proba(response_hot)
                
                # Decode predictions
                encoded_dict = {
                    0: 'GTx Champions',
                    1: 'Risk Balancers',
                    2: 'RWE Seekers'
                }
                prediction_decoded = encoded_dict[prediction[0]]
                


                # Display the results
                st.success("Survey submitted successfully!")
                # reset button
                    

                st.subheader("Survey Results")
                # Using markdown to change the font size and color for the result
                
                st.markdown(
                        """
                        <strong>Prediction:</strong> The HCP is categorized as a <span style='color: green; font-size: 30px;'>{}</span>
                        """.format(prediction_decoded),
                        unsafe_allow_html=True
                    )
                
                # Score visualization
                st.write("#### Category Confidence Scores")
                scores = {
                    "GTx Champions": prediction_score[0][0],
                    "Risk Balancers": prediction_score[0][1],
                    "RWE Seekers": prediction_score[0][2]
                }
                
                # Visual representation of scores
                for category, score in scores.items():
                    st.write(f"**{category}:** {score:.2f}")
                    st.progress(float(score))
                
                # Add description of the predicted category
                st.subheader("What This Means")
                if prediction_decoded == "GTx Champions":
                    st.info("This HCP is likely an early adopter of gene therapies and is confident in prescribing them. They may be good candidates for early engagement with new gene therapy options.")
                elif prediction_decoded == "Risk Balancers":
                    st.info("This HCP is cautious about adopting new therapies and has concerns about safety. They may need additional safety data and reassurance before prescribing gene therapies.")
                else:
                    st.info("This HCP values real-world evidence and needs to see patient outcomes data before adopting new therapies. Sharing case studies and patient outcomes may be effective.")
                
                # Display summary of responses
                with st.expander("View Response Summary"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Respondent Information**")
                        st.write(f"NPI ID: {npi_id}")
                        st.write(f"HCP Name: {reps_name}")
                        st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")
                    
                    with col2:
                        st.write("**Responses**")
                        selected_q1 = []
                        if q1_efficacy: selected_q1.append("Efficacy")
                        if q1_safety: selected_q1.append("Safety")
                        if q1_moa: selected_q1.append("MOA")
                        if q1_dosing: selected_q1.append("Dosing Convenience")
                        st.write(f"**Primary Rationales**: {', '.join(selected_q1) if selected_q1 else 'None selected'}")
                        st.write(f"**Confidence in Prescribing**: {q2_answer}")
                        st.write(f"**Institutional Influence**: {q3_answer}")
                        st.write(f"**Satisfaction with Current Standard of Care**: {q4_answer}")
                        st.write(f"**Key Barriers**: {q5_answer}")
                        st.write(f"**Patient Referral**: {q6_answer}")
                
                # Save the response to a CSV file
                try:
                    # Create response columns dynamically
                    response_dict = {f'Response_{i+1}': [resp] for i, resp in enumerate(response_array)}
                    
                    # Add Q6 to the saved data even though it's not used in the model
                    response_dict['Response_Q6'] = [q6_answer]

                    # Construct DataFrame with timestamp
                    df = pd.DataFrame({
                        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        'NPI_ID': [npi_id],
                        'Reps_Name': [reps_name],
                        **response_dict,
                        'Prediction': [prediction_decoded],
                        'GTx_Champions_Score': [scores["GTx Champions"]],
                        'Risk_Balancers_Score': [scores["Risk Balancers"]],
                        'RWE_Seekers_Score': [scores["RWE Seekers"]]
                    })

                    # Define file path
                    file_path = 'sma_survey_responses.csv'

                    # Check if file exists to write header only once
                    write_header = not os.path.exists(file_path)

                    # Save to CSV
                    df.to_csv(file_path, mode='a', header=write_header, index=False)
                    st.toast("Response saved to database!")
                except Exception as e:
                    st.error(f"Error saving response: {e}")
        
        # Footer
        st.markdown("---")
        st.markdown("© SMA HCP Typing Tool | For Authorised Novartis Reps Only")

if __name__ == "__main__":
    try:
        with open('model.pkl', 'rb') as file:
            model_data = pickle.load(file)
        main(model_data=model_data)
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'model.pkl' is in the same directory as this application.")
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")