import { useState } from 'react';
import Cookies from 'js-cookie';

export function PostButton ({ data, path='/post', defaultText='Submit'}) {
    const submission = Object.freeze({
        Unsubmitted: 0,
        Successful: 1,
        Error: 2
    });

    const [submissionState, setSubmissionState] = useState(submission.Unsubmitted);
    const dataComplete = (Array.isArray(data) && data.some(s => s != 0)) || (!Array.isArray(data) && data != 0);

    const onSubmit = () => {
        if (submissionState == submission.Unsubmitted) {
            if (dataComplete)
                fetch(window.location.pathname + path, { // ensures that primary key is included in fetched URL by using pathname
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': Cookies.get('csrftoken')
                    },
                    body: JSON.stringify(data)
                }).then(response => {
                    setSubmissionState(response.ok ? submission.Successful : submission.Error);
                });
            else
                setSubmissionState(submission.Error);

            setTimeout(() => {setSubmissionState(submission.Unsubmitted);}, 1500);
        }
    };

    switch(submissionState) {
        case submission.Unsubmitted:
            return <div className='button' onClick={onSubmit}>{defaultText}</div>;

        case submission.Successful:
            return <div className='button successful' onClick={onSubmit}>Done!</div>;

        case submission.Error:
            return <div className='button error' onClick={onSubmit}>Error!</div>;
    }
}
