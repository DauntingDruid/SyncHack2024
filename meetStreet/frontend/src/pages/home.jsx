import axios from 'axios';
import { useEffect, useMemo, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { GoHomeFill } from "react-icons/go";
import { FaLocationDot } from "react-icons/fa6";
import { FaUserFriends } from "react-icons/fa";
import { FaCog } from "react-icons/fa";
import { useNavigate } from 'react-router-dom';
import { post } from '../apis/api';


const Home = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState(
    [
      {
          "_id": "d35f8b48-2c7f-4d5c-88a4-5a4f8f0e8c31",
          "name": "Alice Smith",
          "age": 24,
          "gender": "F",
          "password": "password1",
          "profile_picture": "https://randomuser.me/api/portraits/women/1.jpg",
          "radius": 50,
          "interests": ["Reading", "Yoga", "Traveling"],
          "latitude": -33.8871,
          "longitude": 151.1913
      },
      {
          "_id": "f19a6e5c-1b2e-4f6c-a18a-6e5f8a8c31d2",
          "name": "John Doe",
          "age": 26,
          "gender": "M",
          "password": "password2",
          "profile_picture": "https://randomuser.me/api/portraits/men/2.jpg",
          "radius": 100,
          "interests": ["Cycling", "Photography", "Cooking"],
          "latitude": -33.8898,
          "longitude": 151.1857
      },
      {
          "_id": "b12a7f5d-3c4d-4f2e-b27f-3d5f9a9c32e3",
          "name": "Emily Brown",
          "age": 22,
          "gender": "F",
          "password": "password3",
          "profile_picture": "https://randomuser.me/api/portraits/women/3.jpg",
          "radius": 75,
          "interests": ["Dancing", "Hiking", "Art"],
          "latitude": -33.8917,
          "longitude": 151.1950
      },
      {
          "_id": "e23b8c5e-4d5f-4e2f-a38b-4c6f9b9d33f4",
          "name": "Michael Johnson",
          "age": 28,
          "gender": "M",
          "password": "password4",
          "profile_picture": "https://randomuser.me/api/portraits/men/4.jpg",
          "radius": 60,
          "interests": ["Running", "Gaming", "Music"],
          "latitude": -33.8883,
          "longitude": 151.1931
      },
      {
          "_id": "f34c9d6f-5e6f-4f3f-b49c-5d7f9c9e34f5",
          "name": "Sophia Davis",
          "age": 23,
          "gender": "F",
          "password": "password5",
          "profile_picture": "https://randomuser.me/api/portraits/women/5.jpg",
          "radius": 40,
          "interests": ["Painting", "Swimming", "Photography"],
          "latitude": -33.8865,
          "longitude": 151.1902
      },
      {
          "_id": "g45d0e7f-6f7f-4f4f-c50d-6e8f9d9f35f6",
          "name": "James Wilson",
          "age": 27,
          "gender": "M",
          "password": "password6",
          "profile_picture": "https://randomuser.me/api/portraits/men/6.jpg",
          "radius": 80,
          "interests": ["Soccer", "Fishing", "Cooking"],
          "latitude": -33.8887,
          "longitude": 151.1968
      },
      {
          "_id": "h56e1f8g-7g8g-4g5g-d61e-7f9g0e9g36g7",
          "name": "Olivia Martinez",
          "age": 25,
          "gender": "F",
          "password": "password7",
          "profile_picture": "https://randomuser.me/api/portraits/women/7.jpg",
          "radius": 70,
          "interests": ["Traveling", "Yoga", "Music"],
          "latitude": -33.8910,
          "longitude": 151.1924
      },
      {
          "_id": "i67f2g9h-8h9h-4h6h-e72f-8g0h1f0h37h8",
          "name": "Liam Lee",
          "age": 29,
          "gender": "M",
          "password": "password8",
          "profile_picture": "https://randomuser.me/api/portraits/men/8.jpg",
          "radius": 90,
          "interests": ["Photography", "Hiking", "Reading"],
          "latitude": -33.8859,
          "longitude": 151.1907
      },
      {
          "_id": "j78g3h0i-9i0i-4i7i-f83g-9h1i2g1i38i9",
          "name": "Isabella Garcia",
          "age": 21,
          "gender": "F",
          "password": "password9",
          "profile_picture": "https://randomuser.me/api/portraits/women/9.jpg",
          "radius": 65,
          "interests": ["Dancing", "Cooking", "Traveling"],
          "latitude": -33.8869,
          "longitude": 151.1974
      },
      {
          "_id": "k89h4i1j-0j1j-4j8j-g94h-0i2j3h2j39j0",
          "name": "Ethan White",
          "age": 26,
          "gender": "M",
          "password": "password10",
          "profile_picture": "https://randomuser.me/api/portraits/men/10.jpg",
          "radius": 55,
          "interests": ["Running", "Gaming", "Music"],
          "latitude": -33.8885,
          "longitude": 151.1942
      }
  ]
);
  const [displayCard, setDisplayCard] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [location, setLocation] = useState({ lat: 33.8922761, lng: 151.292 });

  console.log("lat lng ", location);
  // console.log("selectedUser", selectedUser);
  // console.log("displayCard", displayCard);
  const getUserInfo = (user) => {
    setDisplayCard(true);
    setSelectedUser(user);
  }
  
  // TO UPDATE
  const mainUser = {
    id: 1,
    name: "John Doe",
    profilePicture: "https://via.placeholder.com/80", // Replace with actual image URL
    coordinates: { lat: 51.505, lng: -0.09 },
  };

  // TO UPDATE
  // useEffect(() => {
  //   const discoverUsers = async () => {
  //     const formData = {};
  //     formData['user_id'] = await localStorage.getItem("userId");
  //     formData['coordinates'] = location;
  //     formData['radius'] = 10000;
  //     console.log("LOCALSTORAGE * ",formData['user_id']);
  //     await post('user/discover', formData).then((data) => {
  //         console.log(data);
  //     });
  //   };
  //   discoverUsers();
  // }, [location]);

  useMemo(() => {
  const getCoords = async () => {
    navigator.geolocation.getCurrentPosition((position) => {
      console.log("position", position);
      setLocation({
        lat: position.coords.latitude,
        lng: position.coords.longitude
      });
    });
  }
  getCoords();
  }, []);



  return (
    <div className="w-full h-full flex justify-center items-center p-12">
      <div className='w-full h-full relative '>
          <MapComponent users={users} mainUser={mainUser} location={location} getUserInfo={getUserInfo} />
        <div className='w-full h-20 absolute bottom-0 mb-12'>
          <div className='w-full h-full justify-center items-center flex'>
            <div className='w-96 h-20 flex justify-around items-center rounded-xl bg-white'>
              <GoHomeFill className='hover:scale-110 active:scale-95 transition-all duration-200' color='#c4c6cc' size={35} />
              <FaUserFriends className='hover:scale-110 active:scale-95 transition-all duration-200' color='#c4c6cc' size={35} />
              <FaLocationDot className='hover:scale-110 active:scale-95 transition-all duration-200' color='#b87dff' size={35} />
              <FaCog className='hover:scale-110 active:scale-95 transition-all duration-200' color='#c4c6cc' size={35} />
            </div>
          </div>
        </div>
      </div>
      {displayCard && 
          <div className="absolute top-1/5 left-1/5 bg-gray-800 text-white rounded-3xl overflow-hidden shadow-lg w-1/3 h-4/5">
            <img
              src="https://images.unsplash.com/photo-1624789389787-91e252ff8dac?q=80&w=3061&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" // Replace with the actual profile image URL
              alt="User profile"
              className="w-full h-full object-cover"
            />
            <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black to-transparent">
              <h2 className="text-2xl font-bold">{selectedUser?.name}</h2>
              <div className="flex items-center space-x-2 text-sm mt-2">
                <span className="inline-flex items-center">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 3a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zM1 5a3 3 0 013-3h12a3 3 0 013 3v12a3 3 0 01-3 3H4a3 3 0 01-3-3V5z" />
                  </svg>
                  <span className="ml-1">Music</span>
                </span>
                <span className="inline-flex items-center">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 3a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zM1 5a3 3 0 013-3h12a3 3 0 013 3v12a3 3 0 01-3 3H4a3 3 0 01-3-3V5z" />
                  </svg>
                  <span className="ml-1">Cinema</span>
                </span>
                <span className="inline-flex items-center">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 3a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zM1 5a3 3 0 013-3h12a3 3 0 013 3v12a3 3 0 01-3 3H4a3 3 0 01-3-3V5z" />
                  </svg>
                  <span className="ml-1">Sport</span>
                </span>
              </div>
              <div className="flex items-center space-x-2 mt-2">
                <span className="inline-flex items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 2a6 6 0 00-6 6c0 6.075 5.823 9.748 5.997 9.875a.5.5 0 00.006 0A.505.505 0 0010 18c.072 0 .14-.014.207-.04C10.177 17.897 16 14.198 16 8a6 6 0 00-6-6zM5 8a5 5 0 1110 0c0 4.383-4.243 7.398-4.998 7.85a.553.553 0 01-.004 0C9.243 15.398 5 12.383 5 8z"
                      clipRule="evenodd"
                    />
                    <path
                      fillRule="evenodd"
                      d="M10 10a2 2 0 100-4 2 2 0 000 4zm0-3a1 1 0 110 2 1 1 0 010-2z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <span className="ml-1">Sydney, Australia</span>
                </span>
              </div>
              <div className="flex justify-between mt-4">
                <button onClick={() => {setDisplayCard(false)}} className="bg-black text-white px-4 py-2 rounded-full">
                  ✕
                </button>
                <button className="bg-purple-500 text-white w-fit px-4 py-2 rounded-full">
                  Message and meet someone new! 
                  {/* ♥ */}
                </button>
              </div>
            </div>
          </div>
      }
    </div>
  );
};

const MapComponent = ({ users, mainUser, location, getUserInfo }) => {
  const [hoveredMarker, setHoveredMarker] = useState(null);
  
  const createCustomIcon = (user) => {
    return L.divIcon({
      html: `<div class="custom-marker">
               <img src="${user.profilePicture}" alt="${user.name}" />
             </div>`,
      className: '',
      iconSize: [50, 50], // Fixed size for the custom marker
      iconAnchor: [25, 25], // Center the icon
      popupAnchor: [0, -25],
    });
  };
  
  const createMainUserIcon = (user) => {
    return L.divIcon({
      html: `<div class="main-user-marker">
               <img src="${user.profilePicture}" alt="${user.name}" />
             </div>`,
      className: '',
      iconSize: [50, 50], // Fixed size for the main user marker
      iconAnchor: [25, 25], // Center the icon
      popupAnchor: [0, -25],
    });
  };
  

  return (
    <MapContainer
      center={[-33.8922705, 151.1911125]} // Default center coordinates
      zoom={13} // Default zoom level
      style={{ width: '100%', height: '90vh', zIndex: 0, borderRadius: '100px' }}
        >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      
      {/* Main User Marker */}
      <Marker
        position={[location.lat, location.lng]}
        icon={createMainUserIcon(mainUser)}
      >
        <Popup className="custom-popup">
          <strong>{mainUser.name}</strong>
        </Popup>
      </Marker>

      {users.map((user) => (
        <Marker
          key={user.id}
          position={[user.latitude, user.longitude]}
          icon={createCustomIcon(user)}
          eventHandlers={{
            mouseover: () => {
              setHoveredMarker(user.id);
            },
            mouseout: () => {
              setHoveredMarker(null);
            },
          }}
        >
          <Popup className="custom-popup">
            <div className='flex flex-col w-full h-full hover:cursor-pointer'>
              <strong>{user.name}</strong>
              <div className=' w-full flex justify-between'>
              <button onClick={() => getUserInfo(user)} className='w-fit h-fit p-1 bg-green-400 rounded-lg hover:scale-105 transition-all duration-150 active:scale-100'>
                Say hi!
              </button>
              </div>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default Home;
