import { HeaderMain } from '../../header.jsx';
import { ReleaseInfo, RatingInfo, ExtraReleaseInfo } from '../../info.jsx';
import { parseJSONScript } from '../../utils.js';
import { StarStylesheet, RatingField } from '../../stars.jsx'

export default function App() {
    const releaseData = parseJSONScript('release-data');
    const lastRatingsData = parseJSONScript('last-ratings-data');
    const loggedIn = parseJSONScript('logged-in');
    const userRating = parseJSONScript('user-rating');
    const avg = parseJSONScript('avg');
    const ratingCount = parseJSONScript('rating-count');

    return <HeaderMain>
        <StarStylesheet/>
        <div className='wrapper'>
            <ExtraReleaseInfo release={releaseData} avg={avg} ratingCount={ratingCount} style={{fontSize: '2em'}}/>

            {loggedIn ? <><RatingField currentRating={userRating}/> <br/> <a className='button' href={window.location.pathname + '/vote'}>Vote</a></>: <></>}
        </div>

        <br/>

        {lastRatingsData.map(r => <RatingInfo rating={r}/>)}

        <br/>

        <div><a className="button" style={{fontSize: '1.5em'}} href={window.location.pathname + '/reviews'}>Reviews</a></div> <br/>
        <div><a className="button" style={{fontSize: '1.5em'}} href={window.location.pathname + '/comments'}>Comments</a></div>
    </HeaderMain>;
}
