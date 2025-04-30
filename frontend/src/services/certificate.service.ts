import {axiosInstance} from "./api.service.ts";
import {urls} from "../constants/urls.ts";

export const CertificateService = {
    async get_certificate(pk:string) {
        const {data} = await axiosInstance.get(urls.users.certificate(pk));
        return data
    },

}