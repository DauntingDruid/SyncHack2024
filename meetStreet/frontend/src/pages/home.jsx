import axios from 'axios';
import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { GoHomeFill } from "react-icons/go";
import { FaLocationDot } from "react-icons/fa6";
import { FaUserFriends } from "react-icons/fa";
import { FaCog } from "react-icons/fa";


const Home = () => {
  const [users, setUsers] = useState([]);
  
  // TO UPDATE
  const mainUser = {
    id: 1,
    name: "John Doe",
    profilePicture: "https://via.placeholder.com/80", // Replace with actual image URL
    coordinates: { lat: 51.505, lng: -0.09 },
  };

  // TO UPDATE
  useEffect(() => {
    // Replace with your actual API endpoint
    axios.get('/api/nearby-users')
      .then(response => {
        setUsers([
          {
            id: 2,
            name: "Jane Smith",
            profilePicture: "https://via.placeholder.com/50", // Replace with actual image URL
            coordinates: { lat: 51.515, lng: -0.09 },
          }
        ]);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
      });
  }, []);

  return (
    <div className="w-full h-full flex justify-center items-center p-12">
      <div className='w-full h-full relative '>
          <MapComponent users={users} mainUser={mainUser} />
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
    </div>
  );
};

const MapComponent = ({ users, mainUser }) => {
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
      center={[mainUser.coordinates.lat, mainUser.coordinates.lng]} // Default center coordinates
      zoom={13} // Default zoom level
      style={{ width: '100%', height: '90vh', zIndex: 0, borderRadius: '100px' }}
        >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      
      {/* Main User Marker */}
      <Marker
        position={[mainUser.coordinates.lat, mainUser.coordinates.lng]}
        icon={createMainUserIcon(mainUser)}
      >
        <Popup className="custom-popup">
          <strong>{mainUser.name}</strong>
        </Popup>
      </Marker>

      {users.map((user) => (
        <Marker
          key={user.id}
          position={[user.coordinates.lat, user.coordinates.lng]}
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
              <button className='w-fit h-fit p-1 bg-green-400 rounded-lg hover:scale-105 transition-all duration-150 active:scale-100'>
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
