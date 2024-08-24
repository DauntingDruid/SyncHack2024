import axios from 'axios';

// Function to handle GET requests
export const get = async (url) => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/" + url);
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

// Function to handle POST requests
export const post = async (url, body) => {
    try {
        const response = await axios.post("http://127.0.0.1:5000/" + url, body);
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

// Function to handle PUT requests
export const put = async (url, body) => {
    try {
        const response = await axios.put("http://127.0.0.1:5000/" + url, body);
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

// Function to handle DELETE requests
export const del = async (url) => {
    try {
        const response = await axios.delete("http://127.0.0.1:5000/" + url);
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

// Function to handle PATCH requests
export const patch = async (url, body) => {
    try {
        const response = await axios.patch("http://127.0.0.1:5000/" + url, body);
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
