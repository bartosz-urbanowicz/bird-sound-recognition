import axios from 'axios'

const Submit = ({ audioBlob, audioUrl }) => {
    const api_url = "http://localhost:5000/"

    function blobToBase64(blob) {
        return new Promise((resolve, _) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result);
          reader.readAsDataURL(blob);
        });
      }

    const handleSubmit = async (e) => {
        e.preventDefault()
        const base64audio = await blobToBase64(audioBlob)
        try {
            const response = await axios.post(api_url, {data: base64audio});
            console.log('Post successful!', response.data);
          } catch (error) {
            console.error('Error while posting:', error);
          }
    }

    return (
        <div>
            <div className="audio-container flex items-center justify-center">
                <audio src={audioUrl} controls></audio>
                <a download href={audioUrl}>
                <i className="fa-solid fa-download m-[0.5em]"></i>
                </a>
            </div>
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
};
export default Submit;