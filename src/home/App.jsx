import { HeaderMain } from '../header.jsx';
import { VerticalReleaseInfo } from '../info.jsx';
import { parseJSONScript } from '../utils.js';
import { useState } from 'react';

export default function App() {
    const whatsHotData = parseJSONScript('whats-hot-data');

    return <HeaderMain>
        <h1>What's Hot</h1>
        <div className='wrapper' style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly'}}>
            {whatsHotData.map(r => <VerticalReleaseInfo release={r}/>)}
        </div>
    </HeaderMain>;
}
