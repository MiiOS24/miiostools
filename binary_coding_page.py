import streamlit as st
import pandas as pd

def create_binary_coding_excel_with_id(input_file, output_file):
    # Load the provided Excel file
    df = pd.read_excel(input_file, sheet_name="Coded Responses")
    coding_schema_df = pd.read_excel(input_file, sheet_name="Coding Schema")

    # Check if 'id' column exists
    if 'id' not in df.columns:
        st.error("The input file does not contain an 'id' column.")
        return

    # Automatically detect the column that holds respondents' answers
    potential_columns = [col for col in df.columns if col not in ['id'] + list(coding_schema_df.columns)]
    if len(potential_columns) == 1:
        answer_column = potential_columns[0]
    else:
        st.write("Available columns: ", potential_columns)
        answer_column = st.selectbox("Please select the column containing the respondents' answers:", options=potential_columns)
        if answer_column not in df.columns:
            st.error(f"The specified column '{answer_column}' does not exist in the dataset.")
            return

    # Convert the coding schema DataFrame into a dictionary
    coding_schema = dict(zip(coding_schema_df["Activity"], coding_schema_df["Code"]))

    # Split the activities into separate columns
    df_split = df[answer_column].str.split(", | and ", expand=True)

    # Create a DataFrame to hold the binary coding for each code
    max_code = max(coding_schema.values())
    binary_df = pd.DataFrame(0, index=df.index, columns=[f"{answer_column}r{i+1}" for i in range(max_code)])

    # Map activities to their codes and set the corresponding columns to 1 where the code is mentioned
    for idx, row in df_split.iterrows():
        for activity in row:
            if pd.notna(activity):  # only proceed if activity is not NaN
                code = coding_schema.get(activity.strip())
                if code is not None:
                    binary_df.at[idx, f"{answer_column}r{code}"] = 1

    # Concatenate the original response, ID, and the binary coding
    binary_df.insert(0, answer_column, df[answer_column])
    binary_df.insert(0, "id", df["id"])

    # Save the final DataFrame to a new worksheet in the same Excel file
    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, sheet_name="Coded Responses", index=False)
        binary_df.to_excel(writer, sheet_name="Binary Coding", index=False)
        coding_schema_df.to_excel(writer, sheet_name="Coding Schema", index=False)

    return output_file

def binary_coding_page():
    st.title("🗃️ manuCODE")
    st.write("This tool allows you to format an XLSX file containing coded responses into a binary format with IDs.")

    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
    if uploaded_file is not None:
        output_file_path = "formatted_binary_coding.xlsx"
        with st.spinner('Formatting your file...'):
            result_file = create_binary_coding_excel_with_id(uploaded_file, output_file_path)
            if result_file:
                st.success("File formatted successfully!")
                st.download_button(
                    label="Download the formatted file",
                    data=open(result_file, "rb"),
                    file_name=output_file_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    st.write("\n")
    st.write("### Example of Input File Structure")
    st.image("img/manucode_example.PNG", caption="Example of the expected structure for the input Excel file.")
    st.image("img/manucode_example_2.PNG", caption="This is how the Coding Schema should be set up.")