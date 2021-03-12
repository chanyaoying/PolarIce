import axios from 'axios';

// use this axios call whenever we need to make authenticated requests to the server
const authAxios = axios.create({
    withCredentials: true,
    crossorigin: true, // CORS 
})

export default authAxios;