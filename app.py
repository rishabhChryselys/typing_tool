import streamlit as st
import pickle
import pandas as pd

def main(model_data):
    
    st.title("Gene Therapy for SMA Patients Survey")
    st.markdown("Please complete the following survey about gene therapy prescribing practices for SMA patients.")
    # npi Id , reps name
    npi_id = st.text_input("NPI ID")
    reps_name = st.text_input("Reps Name")
    # Question 1 - Checkboxes
    st.header("Q1: Primary Rationale for Switching to Gene Therapies")
    st.write("Please select the primary rationale for considering switching to gene therapies:")
    
    q1_efficacy = st.checkbox("Efficacy")
    q1_safety = st.checkbox("Safety")
    q1_moa = st.checkbox("MOA")
    q1_dosing = st.checkbox("Dosing Convenience")
    
    # Question 2 - Radio button
    st.header("Q2: Confidence in Prescribing")
    q2_options = ["Not Confident at All", "Slightly Confident", "Extremely Confident"]
    q2_answer = st.radio(
        "Please select to what extent the HCP is confident in prescribing gene therapy for SMA patients for 1L treatment:",
        options=q2_options
    )
    
    # Question 3 - Radio button
    st.header("Q3: Institutional Influence")
    q3_options = ["Not at all", "Slightly Influential", "Extremely Influential"]
    q3_answer = st.radio(
        "Please indicate to what extent this HCP's institution influences their decision to adopt new therapies like Zolgensma:",
        options=q3_options
    )
    
    # Question 4 - Radio button
    st.header("Q4: Satisfaction with Current Standard of Care")
    q4_options = ["Dissatisfied", "Neutral", "Extremely Satisfied"]
    q4_answer = st.radio(
        "Please select the extent of satisfaction the HCP has with the current standard of care therapies for SMA:",
        options=q4_options
    )
    
    # Question 5 - Radio button
    st.header("Q5: Key Barriers")
    q5_options = [
        "Lack of experience prescribing Zolgensma",
        "Institutional barrier - Lack of GTx capabilities at site",
        "Lack of MDT support at the institute",
        "None of the Above"
    ]
    q5_answer = st.radio(
        "Please select what are the key barriers for HCPs in prescribing gene therapies:",
        options=q5_options
    )
    
    # Question 6 - Radio button
    st.header("Q6: Patient Referral Rate")
    q6_options = ["I do not need to refer my patients", "I may need to refer my patients to a colleague at my institution", "I may need to refer my patients to another institution"]
    q6_answer = st.radio(
        "Do you expect that you would need to refer your patients to receive treatment with Gene Therapy?",
        options=q6_options
    )
    
    # Submit button and response handling
    if st.button("Submit Survey"):
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
        # response_array.append(q6_answer)  # Q6

        
        # Display responses
        st.success("Survey submitted successfully!")
        st.subheader("Survey Responses")
        # Load the saved model and metadata
        
       

        loaded_model = model_data['model']
        loaded_label_encoder = model_data['label_encoder']
        onehot = model_data['one_hot_encoder']

        # Create a DataFrame from the response array
        response_df = pd.DataFrame([response_array], columns=model_data['questions'])
        # One-hot encode the response DataFrame
        # response_hot = pd.get_dummies(response_df, columns=model_data['questions'], prefix=model_data['questions'])
        # print(response_df)
        response_hot = onehot.transform(response_df).toarray()
        # Ensure the response DataFrame has the same columns as the training data
        # response_hot = response_hot.reindex(columns=model_data['questions'], fill_value=0)
        # Make predictions
        prediction = loaded_model.predict(response_hot)
        # Decode the predictions
        # prediction_decoded = loaded_label_encoder.inverse_transform(prediction)
 
        # GTx Chmapions Risk Balancers RWE Seekers
        encoded_dict = {
            0: 'GTx Champions',
            1: 'Risk Balancers',
            2: 'RWE Seekers'
        }
        prediction_decoded = [encoded_dict[pred] for pred in prediction]
        # Display the prediction
        st.write("**Model Prediction:**")
        st.write(f"The model predicts that the HCP is in the {prediction_decoded[0]} category.")
        # # Display the response arrays
        st.write("**Response Array:**")
        st.write(response_array)

        #save the response to a csv file
        import os

        # Ensure npi_id and reps_name are not in list format
        npi_id = npi_id[0] if isinstance(npi_id, list) else npi_id
        reps_name = reps_name[0] if isinstance(reps_name, list) else reps_name
        prediction_decoded = prediction_decoded[0] if isinstance(prediction_decoded, list) else prediction_decoded

        # Create response columns dynamically
        response_dict = {f'Response_{i+1}': [resp] for i, resp in enumerate(response_array)}

        # Construct DataFrame
        df = pd.DataFrame({
            'NPI_ID': [npi_id],
            'Reps_Name': [reps_name],
            **response_dict,  # Expands response columns dynamically
            'Prediction': [prediction_decoded]
        })

        # Define file path
        file_path = 'response.csv'

        # Check if file exists to write header only once
        write_header = not os.path.exists(file_path)

        df.to_csv(file_path, mode='a', header=write_header, index=False)

        
        # # Also show the detailed responses for verification
        # st.write("**Detailed Responses:**")
        
        # st.write("**Q1: Primary Rationale for Switching to Gene Therapies**")
        # q1_selections = []
        # if q1_efficacy:
        #     q1_selections.append("Efficacy")
        # if q1_safety:
        #     q1_selections.append("Safety")
        # if q1_moa:
        #     q1_selections.append("MOA")
        # if q1_dosing:
        #     q1_selections.append("Dosing Convenience")
            
        # if q1_selections:
        #     st.write(f"Selected: {', '.join(q1_selections)}")
        # else:
        #     st.write("No selection made")
            
        # st.write("**Q2: Confidence in Prescribing**")
        # st.write(f"Selected: {q2_answer}")
        
        # st.write("**Q3: Institutional Influence**")
        # st.write(f"Selected: {q3_answer}")
        
        # st.write("**Q4: Satisfaction with Current Standard of Care**")
        # st.write(f"Selected: {q4_answer}")
        
        # st.write("**Q5: Key Barriers**")
        # st.write(f"Selected: {q5_answer}")
        
        # st.write("**Q6: Patient Referral Rate**")
        # st.write(f"Selected: {q6_answer}")
        
if __name__ == "__main__":
    with open('model.pkl', 'rb') as file:
        model_data = pickle.load(file)
    main(model_data=model_data)