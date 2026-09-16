import { parseJSONScript } from '../../utils.js';
import { HeaderMain } from '../../header.jsx';
import { UserInfo, ReleaseRatingInfo } from '../../info.jsx';

export default function App() {
    const user_data = parseJSONScript('user-data');
    const last_ratings_data = parseJSONScript('last-ratings-data');

    return <HeaderMain>
        <div className='wrapper'>
            <UserInfo user={user_data}/>
        </div>

        <br></br>

        {last_ratings_data.map (r => <ReleaseRatingInfo rating={r}/>)}
    </HeaderMain>;
}
