import axios from 'axios';
import {baseUrl, urls} from "../constants/urls.ts";
import Cookies from "js-cookie";
import {ITokenPair} from "../models/token-model/ITokenModel.ts";

export type RegisterData = {
    email: string;
    password: string;
    user: {
        name: string,
        surname: string,
        image: File,
    }
}

export type LoginData = {
    email: string;
    password: string;
}

export const axiosInstance = axios.create({
    baseURL: baseUrl,
    headers: {'Content-Type': 'application/json'},
});

const publicRoutes = [urls.users.create(),]

axiosInstance.interceptors.request.use(req => {
    if (req.url && !publicRoutes.includes(req.url)) {
        const cookie = Cookies.get('token');
        if (cookie) {
            const token: ITokenPair = JSON.parse(cookie);
            req.headers.Authorization = `Bearer ${token.access}`;
        }
    } else if (req.url && publicRoutes.includes(req.url)) {
        req.headers['Content-Type'] = 'multipart/form-data';
    }
    return req;
})

