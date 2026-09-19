import { parseJSONScript } from '../utils.js';
import { HeaderMain } from '../header.jsx';
import { ReleaseInfo } from '../info.jsx';
import { useState } from 'react';

export default function App() {
    const top_5_data = parseJSONScript('top-5-data');

    return <HeaderMain>
        {top_5_data.map ((r, idx) =>
        <div>
            <span>{idx+1}</span>
            <ReleaseInfo release={r}/>
        </div>)}
    </HeaderMain>;
}
