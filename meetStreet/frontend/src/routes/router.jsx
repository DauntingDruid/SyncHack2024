import { BrowserRouter as Router } from 'react-router-dom';
import { Suspense, lazy } from 'react';
import { Route, Routes } from 'react-router-dom';

const WelcomePage = lazy(() => import('../pages/landing.jsx'))
const HomePage = lazy(() => import('../pages/home.jsx'))
const LoginSignup = lazy(() => import('../pages/loginSignup.jsx'))

const MainRouter = () => {

    return (
        <Router>
            <Routes location={location} key={location.pathname}>
                <Route path='/' element={
                    <Suspense fallback={<></>}>
                        <WelcomePage />
                    </Suspense>
                }/>
                <Route path='/home' element={
                    <Suspense fallback={<></>}>
                        <HomePage />
                    </Suspense>
                }/>
                <Route path='/loginSignup' element={
                    <Suspense fallback={<></>}>
                        <LoginSignup />
                    </Suspense>
                }/>
            </Routes>
        </Router>
    )
}

export default MainRouter