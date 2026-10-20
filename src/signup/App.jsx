import { HeaderMain } from '../header.jsx';
import { ReleaseInfo } from '../info.jsx';
import { useState } from 'react';
import Cookies from 'js-cookie';

export default function App() {
    const submission = Object.freeze({
        Unsubmitted: 0,
        Successful: 1,
        Error: 2
    });

    const [submissionState, setSubmissionState] = useState(submission.Unsubmitted);

    async function signupPOST(e) {
        e.preventDefault();

        const data = new FormData(e.target);

        const response = await fetch('./post', {
            method: 'POST',
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            body: data
        });

        if (response.ok) {
            const parsedResponse = await response.json();
            window.location.replace(`/users/${parsedResponse.userId}`);

            setSubmissionState(submission.Successful);
        } else
            setSubmissionState(submission.Error);

        setTimeout(() => {setSubmissionState(submission.Unsubmitted);}, 1500);
    }

    const SubmitButton = () => {
        switch (submissionState) {
            case submission.Unsubmitted:
                return <input className="button" type="submit" value="Sign up"/>;

            case submission.Successful:
                return <input className="button successful" type="submit" value="Sign up"/>;

            case submission.Error:
                return <input className="button error" type="submit" value="Error!"/>;
        }
    };

    return <HeaderMain>
        <h1>Enter your sign-up details:</h1>
        <form enctype="multipart/form-data" onSubmit={signupPOST}>
            <label for="username">Username </label>
            <input type="text" name="username" style={{border: 'none', backgroundColor: '#dddddd'}}/>

            <br/> <br/>

            <label for="location">Location </label>
            <input type="text" name="location" style={{border: 'none', backgroundColor: '#dddddd'}}/>

            <br/> <br/>

            <label for="profile_picture">Profile picture </label>
            <input type="file" name="profile_picture" accept="image/*"/>

            <br/> <br/>

            <SubmitButton/>
        </form>
    </HeaderMain>
}
