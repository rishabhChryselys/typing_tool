'''

Last Modified: 2025-02-28
Author: Satyam, Vishesh, Rishabh

'''


import streamlit as st
import pickle
import pandas as pd
import numpy as np
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
            st.image("Gene Therapy.png", width=300)
            st.title("Welcome to the Gene Therapy HCP Typing Tool")
            
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


def predict_segment(input_data, model):
    input_df = pd.DataFrame(input_data)
    prediction = model.predict(input_df)[0]
    return prediction


def main(model_data):
    # Check if we need to show the welcome screen
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
        show_welcome_screen()
    else:
        # Sidebar for information
        with st.sidebar:
            st.image("Gene Therapy.png", width=200)
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
        st.title("Gene Therapy HCP Typing Tool")
        st.markdown("Please complete the following survey to determine the attitudinal segments for an HCP.")
        
        # Create two columns for the initial inputs
        col1, col2, col3 = st.columns(3)
        with col1:
            # NPI 10 digit number
            npi_id = st.text_input("NPI ID", placeholder="Enter NPI ID", max_chars=10, help="Enter the 10-digit NPI ID")
        with col2:
            reps_first_name = st.text_input("HCP First Name", placeholder="Enter representative's fast name")
        with col3:
            reps_last_name = st.text_input("HCP Last Name", placeholder="Enter representative's last name")
        
        col_1, col_2 = st.columns(2)
        with col_1:
            HCP_practicing_id = st.text_input("HCP Practicing ID", placeholder="Enter HCP ID")
        with col_2:
            # drop down for HCP practicing site
            HCP_practicing_site = st.selectbox("HCP Practicing Site", ["Hospital", "Clinic", "Private Practice", "Other"])
        # Create a form for the survey
        with st.form("survey_form"):
            input_data = {}
            # Question 1 - Checkboxes
            st.header("Q1: Treatment Drivers")
            st.markdown("For your SMA patients (> 2 years old), Please select the primary rationale considered for switching to gene therapies from existing therapies  \n (Select all Applicable options):")
            input_data['Q1_1'] = [0]
            input_data['Q1_2'] = [0]
            input_data['Q1_3'] = [0]
            input_data['Q1_4'] = [0]
            
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox("Efficacy", help="Select if efficacy is a primary rationale"): input_data['Q1_1'] = [1]
                if st.checkbox("Safety", help="Select if safety is a primary rationale"): input_data['Q1_2'] = [1]
            with col2:
                if st.checkbox("MOA (Mechanism of Action)", help="Select if mechanism of action is a primary rationale"): input_data['Q1_3'] = [1]
                if st.checkbox("Dosing Convenience", help="Select if dosing convenience is a primary rationale") : input_data['Q1_4'] = [1]
            
            st.markdown("---")
            
            # Question 2 - Radio button
            st.header('Q2: Belief in Gene Therapy')
            st.markdown('Please state your agreement with "Gene therapy should be 1st line treatment for my SMA patient"')
            
            input_data['Q2_0'] = [0]
            input_data['Q2_1'] = [0]
            input_data['Q2_2'] = [0]
            q2_options = [" I Agree", "I am Neutral", "I Disagree"]
            q2_answer = st.radio(
                "Agrement Level",
                options=q2_options,
                key="q2_radio",
                index= None
            )
            if q2_answer: input_data[f'Q2_{q2_options.index(q2_answer)}'] = [1]
            
            st.markdown("---")
            
            # Question 3 - Radio button
            st.header("Q3: Current S/E Satisfaction")
            st.markdown("Please select the level of satisfaction you have with the Spinraza and Evrysdi for SMA patients > 2 years old")
            
            input_data['Q4_0'] = [0]
            input_data['Q4_1'] = [0]
            input_data['Q4_2'] = [0]
            q3_options = ["Extremely Satisfied", "Neutral", "Dissatisfied"]
            q3_answer = st.radio(
                "Satisfaction Level",
                options=q3_options,
                key="q3_radio",
                index = None
            )
            if q3_answer: input_data[f'Q4_{q3_options.index(q3_answer)}'] = [1]
            
            st.markdown("---")
            
            # Question 4 - Radio button
            st.header("Q4: Barriers in Prescribing Gene Therapy")
            st.markdown(" Please select what are the key barriers in prescribing gene therapies in SMA")
            
            input_data['Q5_0'] = [0]
            input_data['Q5_1'] = [0]
            input_data['Q5_2'] = [0]
            input_data['Q5_3'] = [0]

            q4_options = [
                "Lack of experience prescribing Zolgensma", 
                "Gene Therapy capabilities at site are not good enough (e.g. Financial Barriers, Pre and Post Monitoring Capabilities, Administration)", 
                "MDT collaboration needs to be stronger", 
                "No Barriers / Institution is well equipped to administer Gene theapy"
            ]
            q4_answer = st.radio(
                "Key Barrier",
                options=q4_options,
                key="q4_radio",
                index = None
            )
            if q4_answer: input_data[f'Q5_{q4_options.index(q4_answer)}'] = [1]
            
            st.markdown("---")
            
            # Question 5 - Radio button
            st.header("Q5: Experience with Gene Therapy")
            st.markdown("State your primary role while treating SMA patients with Gene Therapies:")

            input_data['Q7_0'] = [0]
            input_data['Q7_1'] = [0]
            input_data['Q7_2'] = [0]

            q5_options = [ 
                "I prescribe and administer Gene therapies ", 
                "I need to refer my patients to a colleague at my institution  ", 
                "I need to refer my patients to another institution "
            ]
            q5_answer = st.radio(
                "Key Barrier",
                options=q5_options,
                key="q5_radio",
                index = None
            )
            if q5_answer: input_data[f'Q7_{q5_options.index(q5_answer)}'] = [1]

            # Submit button with standard styling
            submit_col1, submit_col2 = st.columns([15,5])
            with submit_col2:
                submit_button = st.form_submit_button("Submit Survey")



        # Handle form submission
        if submit_button:
            if not npi_id or not reps_first_name or q2_answer == None or q3_answer == None or q4_answer == None or q5_answer == None:
                st.error("Please select an option for all questions before submitting.")
            else:
                # Prepare the input data for prediction
                segment = predict_segment(input_data, model_data)

                
                
                # Decode predictions
                encoded_dict = {
                    1: 'GTx Champions',
                    2: 'Risk Balancers',
                    3: 'RWE Seekers'
                }
                prediction_decoded = encoded_dict[segment]
                prediction_score = model_data.predict_proba(pd.DataFrame(input_data))
                


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
                        st.write(f"HCP First Name: {reps_first_name}")
                        st.write(f"HCP Last Name: {reps_last_name}")
                        st.write(f"HCP Practicing ID: {HCP_practicing_id}")
                        st.write(f"HCP Practicing Site: {HCP_practicing_site}")
                        st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")
                    
                    with col2:
                        st.write("**Responses**")
                        selected_q1 = []
                        for key, value in input_data.items():
                            # print(key,value)
                            if key == 'Q1_1' and value == [1]:
                                selected_q1.append("Efficiency")
                            elif key == 'Q1_2' and value == [1]:
                                selected_q1.append("Safety")
                            elif key == 'Q1_3' and value == [1]:
                                selected_q1.append("MOA")
                            elif key == 'Q1_4' and value == [1]:
                                selected_q1.append("Dosing")
                        # print(selected_q1)
                        st.write(f"Q1: {', '.join(selected_q1)}")
                        st.write(f"Q2: {q2_answer}")
                        st.write(f"Q3: {q3_answer}")
                        st.write(f"Q4: {q4_answer}")
                        st.write(f"Q5: {q5_answer}")

                
                # Save the response to a CSV file
                try:
                    # Create response columns dynamically
                    response_dict = {}
                    response_dict['Q1_1'] = np.nan
                    response_dict['Q1_2'] = np.nan
                    response_dict['Q1_3'] = np.nan
                    response_dict['Q1_4'] = np.nan

                    for key, value in input_data.items():
                        if key == 'Q1_1' and value == [1]:
                            response_dict['Q1_1'] = "Efficiency"
                        elif key == 'Q1_2' and value == [1]:
                            response_dict['Q1_2'] = "Safety"
                        elif key == 'Q1_3' and value == [1]:
                            response_dict['Q1_3'] = "MOA"
                        elif key == 'Q1_4' and value == [1]:
                            response_dict['Q1_4'] = "Dosing"
                    response_dict['Q3'] = q3_answer
                    response_dict['Q4'] = q4_answer
                    response_dict['Q5'] = q5_answer


                    

                    # Construct DataFrame with timestamp
                    df = pd.DataFrame({
                        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        'NPI_ID': [npi_id],
                        'Reps_First_Name': [reps_first_name],
                        'Reps_Last_Name': [reps_last_name],
                        'HCP_Practicing_ID': [HCP_practicing_id],
                        'HCP_Practicing_Site': [HCP_practicing_site],
                        **response_dict,
                        'Prediction': [prediction_decoded],
                        'GTx_Champions_Score': [round(scores["GTx Champions"], 2)],
                        'Risk_Balancers_Score': [round(scores["Risk Balancers"], 2)],
                        'RWE_Seekers_Score': [round(scores["RWE Seekers"], 2)]
                    })
                    
                    # Define file path
                    file_path = 'sma_survey_responses.csv'

                    # Check if file exists
                    write_header = not os.path.exists(file_path)


                    # Save to CSV
                    df.to_csv(file_path, mode='a', header=write_header, index=False)
                    st.toast("Response saved to database!")
                except Exception as e:
                    st.error(f"Error saving response: {e}")
        
        # Footer
        st.markdown("---")
        st.markdown("©2025 SMA Gene Therapy HCP Typing Tool | For Authorised Novartis Reps Only")

if __name__ == "__main__":
    try:
        with open('model.pkl', 'rb') as file:
            model_data = pickle.load(file)
        main(model_data=model_data)
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'model.pkl' is in the same directory as this application.")
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")