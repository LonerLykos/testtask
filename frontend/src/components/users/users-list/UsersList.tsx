import {useEffect, useState} from "react";
import {ProfileService} from "../../../services/profile.service.ts";
import {IProfile} from "../../../models/profile/IProfile.ts";

export const UsersList = () => {

    const [profile, setProfile] = useState<IProfile[]>()

    useEffect(() => {
        const fetch = async ()  => {
            const {data} = await ProfileService.get_all()
            setProfile(data)
        }

        fetch()
    }, []);

    console.log(profile)
    return (
        <div>

        </div>
    );
};
