import {useEffect, useState} from "react";
import {ProfileService} from "../../../services/profile.service.ts";

export const UsersList = () => {

    const [profile, setProfile] = useState()

    useEffect(() => {
        const fetch = async ()  => {
            const {data} = await ProfileService.get_all()
            setProfile(data)
        }

        fetch()
    }, []);


    return (
        <div>
            {profile.map}
        </div>
    );
};
