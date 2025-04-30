import {useLocation} from "react-router-dom";
import {CertificateService} from "../../services/certificate.service.ts";


const CertificatePage = () => {

    const location = useLocation().pathname
    const pk = location.split('/')[2]


    const myHandler = async () => {
        try {
            const data = await CertificateService.get_certificate(pk)
            console.log(data);
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <>
            <button onClick={myHandler}>Register</button>
            <div></div>
        </>

    );
};

export default CertificatePage;