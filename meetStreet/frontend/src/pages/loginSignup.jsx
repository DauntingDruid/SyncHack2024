import { useState } from 'react';
import signup from "../assets/imgs/signup.svg";
import { get, post } from '../apis/api';
import { useNavigate } from 'react-router-dom';

const AuthPage = () => {
    const navigate = useNavigate();
    const [isLogin, setIsLogin] = useState(true);
    const [userInfo, setUserInfo] = useState({
        name: '',
        email: '',
        age: '',
        gender: '',
        password: '',
        profile_picture: '',
        radius: 0,
        interests: '',
    });

    console.log("userInfo", userInfo);

    const toggleForm = () => {
        setIsLogin(!isLogin);
    };

    const updateName = (e) => {
        setUserInfo({ ...userInfo, name: e.target.value });
    };

    const updateEmail = (e) => {
        setUserInfo({ ...userInfo, email: e.target.value });
    };

    const updatePassword = (e) => {
        setUserInfo({ ...userInfo, password: e.target.value });
    };

    const updateProfilePicture = (e) => {
        setUserInfo({ ...userInfo, profile_picture: e.target.files[0] });
    };

    const updateRadius = (e) => {
        setUserInfo({ ...userInfo, radius: e.target.value });
    };

    const updateInterests = (e) => {
        setUserInfo({ ...userInfo, interests: e.target.value });
    };

    const loginUser = async () => {
        const formData = {}
        formData['name'] = userInfo.name;
        // formData['password'] = userInfo.password;
        console.log(formData);
        await post('friend/profile/login', formData).then((data) => {
            console.log(data);
            
            localStorage.setItem("userId", data)
        });
    };

    const signupUser = async () => {
        const formData = {};
        formData['name'] = userInfo.name;
        formData['password'] = userInfo.password;
        formData['gender'] = userInfo.gender;
        formData['age'] = userInfo.age;
        formData['profile_picture'] = userInfo.profile_picture;
        formData['radius'] = userInfo.radius;
        formData['interests'] = userInfo.interests;
        console.log(formData);
        await post('friend/profile/signup', formData).then((data) => {
            console.log(data);
            
            localStorage.setItem("userInfo", data)
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (isLogin) {
            loginUser();
        } else {
            signupUser();
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-[#F4F1EB] p-4">
            <div className="bg-white w-full max-w-md p-8 rounded-xl shadow-lg">
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
                    {isLogin ? 'Login' : 'Sign Up'}
                </h2>
                <form onSubmit={handleSubmit}>
                    {!isLogin ? (
                        <>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="name">
                                    Name
                                </label>
                                <input
                                    type="text"
                                    id="name"
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none focus:bg-white"
                                    placeholder="Enter your name"
                                    required
                                    onChange={updateName}
                                />
                            </div>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="password">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    id="password"
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none focus:bg-white"
                                    placeholder="Enter your password"
                                    required
                                    onChange={updatePassword}
                                />
                            </div>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="profile_picture">
                                    Profile Picture
                                </label>
                                <input
                                    type="file"
                                    id="profile_picture"
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none focus:bg-white"
                                    onChange={updateProfilePicture}
                                />
                            </div>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="radius">
                                    Radius (km)
                                </label>
                                <input
                                    type="number"
                                    id="radius"
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none focus:bg-white"
                                    placeholder="Set radius"
                                    onChange={updateRadius}
                                />
                            </div>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="interests">
                                    Interests
                                </label>
                                <input
                                    type="text"
                                    id="interests"
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none focus:bg-white"
                                    placeholder="Enter your interests (comma-separated)"
                                    onChange={updateInterests}
                                />
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="name">
                                    Name
                                </label>
                                <input
                                    type="text"
                                    id="name"
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none focus:bg-white"
                                    placeholder="Enter your name"
                                    required
                                    onChange={updateName}
                                />
                            </div>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="password">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    id="password"
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 text-gray-800 focus:outline-none focus:bg-white"
                                    placeholder="Enter your password"
                                    required
                                    onChange={updatePassword}
                                />
                            </div>
                        </>
                    )}

                    <div className="flex items-center justify-between">
                        <button
                            type="submit"
                            className="bg-[#6B47DC] text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:bg-[#5842BB] transition-colors duration-300"
                        >
                            {isLogin ? 'Login' : 'Sign Up'}
                        </button>
                    </div>
                </form>
                <div className="text-center mt-4">
                    <button
                        onClick={toggleForm}
                        className="text-[#6B47DC] hover:underline"
                    >
                        {isLogin ? "Don't have an account? Sign Up" : 'Already have an account? Login'}
                    </button>
                </div>
            </div>
            <div>
                <img src={signup} alt="si" className='w-96 ml-8' />
            </div>
        </div>
    );
};

export default AuthPage;