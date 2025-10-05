import streamlit as st
from pathlib import Path
import tempfile
import shutil
from sorawm.core import SoraWM


def main():
    st.set_page_config(
        page_title="Sora Watermark Cleaner",
        page_icon="🎬",
        layout="centered"
    )

    st.title("🎬 Sora Watermark Cleaner")
    st.markdown("Remove watermarks from Sora-generated videos with ease")

    # Initialize SoraWM
    if 'sora_wm' not in st.session_state:
        with st.spinner("Loading AI models..."):
            st.session_state.sora_wm = SoraWM()

    st.markdown("---")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your video",
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Select a video file to remove watermarks"
    )

    if uploaded_file is not None:
        # Display video info
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        st.video(uploaded_file)

        # Process button
        if st.button("🚀 Remove Watermark", type="primary", use_container_width=True):
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir)

                # Save uploaded file
                input_path = tmp_path / uploaded_file.name
                with open(input_path, 'wb') as f:
                    f.write(uploaded_file.read())

                # Process video
                output_path = tmp_path / f"cleaned_{uploaded_file.name}"

                try:
                    with st.spinner("🔄 Processing video... This may take a few minutes."):
                        st.session_state.sora_wm.run(input_path, output_path)

                    st.success("✅ Watermark removed successfully!")

                    # Display result
                    st.markdown("### Result")
                    st.video(str(output_path))

                    # Download button
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download Cleaned Video",
                            data=f,
                            file_name=f"cleaned_{uploaded_file.name}",
                            mime="video/mp4",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(f"❌ Error processing video: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Built with ❤️ using Streamlit and AI</p>
            <p><a href='https://github.com/linkedlist771/SoraWatermarkCleaner'>GitHub Repository</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
