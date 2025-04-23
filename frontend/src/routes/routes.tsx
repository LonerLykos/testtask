import {useRoutes} from "react-router-dom";
import {lazy, Suspense} from "react";
import {AppRoutes} from "./constants.ts";

const Main = lazy(() => import ('../pages/main/MainPage.tsx'));
const Register = lazy(() => import ('../pages/register/RegisterPage.tsx'));
const Login = lazy(() => import ('../pages/login/LoginPage.tsx'));
const Certificate = lazy(()=> import('../pages/certificate/CertificatePage.tsx'));
const Users = lazy(()=> import ('../pages/users/UsersPage.tsx'))

export const RoutesComponent = () => useRoutes([
    {
        element: (
            <Suspense fallback={<div>Loading...</div>}>
                <Main/>
            </Suspense>
        ),
        path: AppRoutes.root,
        index: true
    },
    {
        element: (
            <Suspense fallback={<div>Loading...</div>}>
                <Register/>
            </Suspense>
        ),
        path: AppRoutes.register,
    },
    {
        element: (
            <Suspense fallback={<div>Loading...</div>}>
                <Login/>
            </Suspense>
        ),
        path: AppRoutes.auth.login,
    },
    {
        element: (
            <Suspense>
                <Certificate/>
            </Suspense>
        ),
        path: AppRoutes.users.update(),
    },
    {
        element: (
            <Suspense>
                <Users/>
            </Suspense>
        ),
        path: AppRoutes.users.all,
    },
]);
