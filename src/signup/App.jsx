import { HeaderMain } from '../header.jsx';
import { ReleaseInfo } from '../info.jsx';
import Cookies from 'js-cookie';

function signupPOST(e) {
    e.preventDefault();

    const data = new FormData(e.target);

    fetch('./post', {
        method: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        body: data
    }).then(response => {
        if (response.ok)
            window.location.replace(`/users/${response.formData().get('userId')}`);
    });
}

export default function App() {
    return <HeaderMain>
        <h1>Enter your sign-up details:</h1>
        <form enctype="multipart/form-data" onSubmit={signupPOST}>
            <label for="username">Username </label>
            <input type="text" name="username" style={{border: 'none', backgroundColor: '#dddddd'}}></input>

            <br></br> <br></br>

            <label for="location">Location </label>
            <input type="text" name="location" style={{border: 'none', backgroundColor: '#dddddd'}}></input>

            <br></br> <br></br>

            <label for="profile_picture">Profile picture: </label>
            <input type="file" name="profile_picture" accept="image/*"></input>

            <br></br> <br></br>

            <input className="button" type="submit" value="Sign up"></input>
        </form>
    </HeaderMain>
}
