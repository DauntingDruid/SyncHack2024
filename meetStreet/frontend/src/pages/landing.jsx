import bg_img from "../assets/imgs/meeting.jpg"
import { useNavigate } from "react-router-dom";
// import { useDispatch } from 'react-redux';

const WelcomePage = () => {
  const navigate = useNavigate();
  // const dispatch = useDispatch();

  const routeToPage = () =>{
    navigate(`/home`);
  }


  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-white p-4">
      <img src={bg_img} alt="bg-img" className='w-full h-full absolute' />
      <div className="w-full h-[700px] bg-[#D4C1FB] bg-opacity-60 rounded-3xl shadow-lg text-left flex flex-col justify-start items-center p-16 animate-tilt">
        <div className='flex justify-center items-center text-7xl font-semibold text-white'>
          Meet Street
        </div>
        <div className='w-full text-start flex items-center text-5xl mt-16 font-semibold text-white'>
          Find Your<br />
          Perfect Match
        </div>
        <div className='w-full text-start text-2xl text-gray-500 text-opacity-75 mt-8'>
          Get Ready to meet amazing<br/>
          people and make meaningful<br/>
          connection!
        </div>
        <div className='w-full mt-auto justify-start items-center'>
          <button onClick={routeToPage} className="bg-[#F3E756] text-black md:text-xl font-semibold py-6 px-9 rounded-lg shadow-md hover:bg-yellow-400 active:scale-95  transition-all duration-300">
            Get started &rarr;
          </button>
        </div>
      </div>
    </div>
  );
};

export default WelcomePage;
