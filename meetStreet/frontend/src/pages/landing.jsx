import { useNavigate } from "react-router-dom";
import img1 from "../assets/imgs/img1.jpg";
import img2 from "../assets/imgs/img2.jpg";
import img3 from "../assets/imgs/img3.jpg";
// import { useDispatch } from 'react-redux';

const WelcomePage = () => {
    const navigate = useNavigate();
  // const dispatch = useDispatch();

  const routeToPage = () =>{
    navigate(`/loginSignup`);
  }

    return (
      <div className="container mx-auto p-6">
        {/* Header */}
        <header className="flex justify-between items-center mb-10 border-b-2 py-1">
          <h1 className="text-3xl font-bold">Meet Street</h1>
          <nav className="space-x-4">
            <a href="#home" className="text-gray-600">Home</a>
            <a href="#about" className="text-gray-600">About</a>
            <a href="#contact" className="text-gray-600">Contact</a>
          </nav>
          <button onClick={routeToPage} className="hidden md:block text-white bg-[#9865ff] px-4 py-2 rounded-full">Login / Signup &rarr;</button>
        </header>
  
        {/* Main Content */}
        <div className="text-center md:text-left mb-12 mt-20">
          <h2 className="text-4xl md:text-6xl font-bold leading-tight mb-4 text-[#bc9aff]">
          Create your unique profile
          </h2>
          <p className="text-xl text-gray-500 mb-3 mt-6">
            Get ready to meet amazing people and make meaningful connections! 
          </p>
          <p className="text-xl text-gray-500 mb-6">
            Find your perfect match and start your journey today!
          </p>
        </div>
  
        {/* Images and Tags Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="relative">
            <img src={img1} alt="Art 1" className="rounded-lg object-cover w-full h-full" />
          </div>
          <div className="relative">
            <img src={img2} alt="Art 2" className="rounded-full object-cover w-full h-full" />
          </div>
          <div className="relative">
            <img src={img3} alt="Art 3" className="rounded-lg object-cover w-full h-full" />
            <button onClick={routeToPage} className="bg-[#F3E756] absolute bottom-2 right-2 text-black md:text-xl font-semibold py-6 px-9 rounded-lg shadow-md hover:bg-yellow-400 active:scale-95  transition-all duration-300">
              Get started &rarr;
            </button>
          </div>
        </div>
      </div>
    );
  };
  
  export default WelcomePage;
  

// const WelcomePage = () => {
//   const navigate = useNavigate();
//   // const dispatch = useDispatch();

//   const routeToPage = () =>{
//     navigate(`/loginSignup`);
//   }


//   return (
//     <div className="min-h-screen w-full flex items-center justify-center bg-white p-4">
//       <img src={bg_img} alt="bg-img" className='w-full h-full absolute' />
//       <div className="w-full h-[700px] bg-[#D4C1FB] bg-opacity-60 rounded-3xl shadow-lg text-left flex flex-col justify-start items-center p-16 animate-tilt">
//         <div className='flex justify-center items-center text-7xl font-semibold text-white'>
//           Meet Street
//         </div>
//         <div className='w-full text-start flex items-center text-5xl mt-16 font-semibold text-white'>
//           Find Your<br />
//           Perfect Match
//         </div>
//         <div className='w-full text-start text-2xl text-gray-500 text-opacity-75 mt-8'>
//           Get Ready to meet amazing<br/>
//           people and make meaningful<br/>
//           connection!
//         </div>
//         <div className='w-full mt-auto justify-start items-center'>
//           <button onClick={routeToPage} className="bg-[#F3E756] text-black md:text-xl font-semibold py-6 px-9 rounded-lg shadow-md hover:bg-yellow-400 active:scale-95  transition-all duration-300">
//             Get started &rarr;
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default WelcomePage;
