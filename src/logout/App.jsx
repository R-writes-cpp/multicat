import { HeaderMain } from '../header.jsx'
import { ReleaseInfo } from '../info.jsx'
import Cookies from 'js-cookie'

function logoutPOST(e) {
    e.preventDefault();

    const data = new FormData(e.target);

    fetch('./post', {
        method: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'same-origin'
    }).then(response => {
        if (response.ok)
            window.location.replace('/')
    });
}

export default function App() {
    return <HeaderMain>
        <h1>Are you sure you want to log out?</h1>
        <form onSubmit={logoutPOST}>
            <input className="button" type="submit" value="Log out"></input>
        </form>
    </HeaderMain>
}
