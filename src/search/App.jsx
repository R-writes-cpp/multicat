import { HeaderMain } from '../header.jsx'
import { ReleaseInfo } from '../info.jsx'

const top_5_data = JSON.parse(document.getElementById('top-5-data').textContent);

export default function App() {
    return <HeaderMain>
        <h1>Search Results</h1>
        {top_5_data.map(r => <ReleaseInfo release={r}/>)}
    </HeaderMain>
}
