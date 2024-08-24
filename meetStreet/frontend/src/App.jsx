import { useState } from 'react'
import './App.css'
import HomePage from './pages/home'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='w-full h-full flex justify-center items-center'>
        <HomePage />
    </div>
  )
}

export default App
