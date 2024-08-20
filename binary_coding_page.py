import streamlit as st
import pandas as pd
import numpy as np

def create_binary_coding_excel_with_id(input_file, output_file):
    # Load the provided Excel file
    try:
        df = pd.read_excel(input_file, sheet_name="Coded Responses")
        coding_schema_df = pd.read_excel(input_file, sheet_name="Coding Schema")
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")
        return None

    # Check if 'id' column exists
    if 'id' not in df.columns:
        st.error("The input file does not contain an 'id' column.")
        return None

    # Identify the answer column (assuming it's the first non-'id' column)
    answer_column = [col for col in df.columns if col != 'id'][0]

    # Convert the coding schema DataFrame into a dictionary
    coding_schema = dict(zip(coding_schema_df["Activity"], coding_schema_df["Code"]))

    # Get all unique codes
    all_codes = sorted(set(coding_schema.values()))

    # Create a DataFrame to hold the binary coding for each code
    binary_df = pd.DataFrame(0, index=df.index, columns=[f"{answer_column}r{code}" for code in all_codes])

    # Function to process each row
    def process_row(row):
        binary = np.zeros(len(all_codes))
        for i in range(1, 6):  # Assuming there are at most 5 code columns
            code_col = f"Code {i}"
            if code_col in row and pd.notna(row[code_col]):
                code = int(row[code_col])
                if code in all_codes:
                    binary[all_codes.index(code)] = 1
        return binary

    # Apply the processing function to each row
    binary_data = np.array(list(df.apply(process_row, axis=1)))
    binary_df = pd.DataFrame(binary_data, columns=[f"{answer_column}r{code}" for code in all_codes])

    # Concatenate the original response, ID, and the binary coding
    result_df = pd.concat([df[['id', answer_column]], binary_df], axis=1)

    # Save the final DataFrame to a new worksheet in the same Excel file
    try:
        with pd.ExcelWriter(output_file) as writer:
            df.to_excel(writer, sheet_name="Coded Responses", index=False)
            result_df.to_excel(writer, sheet_name="Binary Coding", index=False)
            coding_schema_df.to_excel(writer, sheet_name="Coding Schema", index=False)
    except Exception as e:
        st.error(f"Error writing Excel file: {str(e)}")
        return None

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
            else:
                st.error("An error occurred during file processing.")

    st.write("\n")
    st.write("### Example of Input File Structure")
    st.image("img/manucode_example.PNG", caption="Example of the expected structure for the input Excel file.")
    st.image("img/manucode_example_2.PNG", caption="This is how the Coding Schema should be set up.")

if __name__ == "__main__":
    binary_coding_page()