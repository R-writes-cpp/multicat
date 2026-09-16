import { HeaderMain } from '../header.jsx'
import { ReleaseInfo } from '../info.jsx'
import Cookies from 'js-cookie'

function loginPOST(e) {
    e.preventDefault();

    const data = new FormData(e.target);

    fetch('./post', {
        method: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'same-origin',
        body: data.get('username')
    }).then(response => {
        if (response.ok)
            window.location.replace('/users')
    });
}

export default function App() {
    return <HeaderMain>
        <h1>Log in</h1>
        <form onSubmit={loginPOST}>
            <input type="text" name="username" style={{border: 'none', backgroundColor: '#dddddd'}}></input>
            <input className="button" type="submit" value="Submit"></input>
        </form>
    </HeaderMain>
}
