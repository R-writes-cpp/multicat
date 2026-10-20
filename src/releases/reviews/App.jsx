import { HeaderMain } from '../../header.jsx';
import { ExtraReleaseInfo, RatingInfo } from '../../info.jsx';
import { TextSubmit } from '../../textsubmit.jsx';
import { parseJSONScript } from '../../utils.js';

export default function App() {
    const releaseData = parseJSONScript('release-data');
    const lastReviewsData = parseJSONScript('last-reviews-data');
    const loggedIn = parseJSONScript('logged-in');
    const avg = parseJSONScript('avg');
    const ratingCount = parseJSONScript('rating-count');

    return <HeaderMain>
        <div className='wrapper'>
            <ExtraReleaseInfo release={releaseData} avg={avg} ratingCount={ratingCount} style={{fontSize: '2em'}}/>
        </div>

        <br/>

        <TextSubmit/>

        {lastReviewsData.map(r =>
        <>
            <RatingInfo rating={r.rating}/>
            <div style={{maxWidth: '50vw', margin: '0 auto', overflowWrap: 'anywhere', fontSize: '1.2em'}}>{r.text}</div>
            <br/> <br/>
        </>)}
    </HeaderMain>;
}
