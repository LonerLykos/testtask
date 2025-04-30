import {Link, useLocation, useNavigate} from "react-router-dom";
import classNames from "classnames";

export const Menu = () => {

    const status = 1
    const navigate = useNavigate();
    const location = useLocation();

    if (!status){
        navigate('/login');
        return null;
    }

    const isActive = (path: string) => location.pathname === path;
    return (
        <div className={classNames('menu-wrapper', {'login': status}, {'unlogin': !status})}>
            <>
                <ul className={classNames('navigate')}>
                    <li className={classNames('pages')}>
                        {/*<button onClick={handleLogout}>Logout</button>*/}
                    </li>
                    <li className={classNames('pages', {'active': isActive('/')})}><Link to={'/'}>Main</Link></li>
                    <li className={classNames('pages', {'active': isActive('/register')})}><Link to={'/register'}>Register</Link></li>
                    <li className={classNames('pages', {'active': isActive('/auth/login')})}><Link to={'/auth/login'}>Login</Link></li>
                    <li className={classNames('pages', {'active': isActive('/users')})}><Link to={'/users'}>Users</Link></li>
                    <li className={classNames('pages', {'active': isActive('/users/3')})}><Link to={'/users/3'}>Certificate</Link></li>
                </ul>
            </>
        </div>
    )
};
