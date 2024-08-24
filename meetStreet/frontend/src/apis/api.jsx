// api.jsx

// Function to handle GET requests
export const get = async (url) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/"+url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

// Function to handle POST requests
export const post = async (url, body) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/"+url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

// Function to handle PUT requests
export const put = async (url, body) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/"+url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

// Function to handle DELETE requests
export const del = async (url) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/"+url, {
            method: 'DELETE',
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
// Function to handle PATCH requests
export const patch = async (url, body) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/"+url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};