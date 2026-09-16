import { HeaderMain } from '../../header.jsx';
import { ReleaseInfo } from '../../info.jsx';
import { parseJSONScript } from '../../utils.js';
import { useState } from 'react';
import { StarStylesheet, VotingFieldGroup } from '../../stars.jsx'

export default function App() {
    const releaseData = parseJSONScript('release-data');
    const descriptorVotesData = parseJSONScript('descriptor-votes-data');
    const loggedIn = parseJSONScript('logged-in');

    const descriptorToScore = Array(18).fill(0);

    descriptorVotesData.forEach(d => {
        descriptorToScore[d.descriptor] = d.score;
    });

    return <HeaderMain>
        <StarStylesheet/>
        <div className='wrapper'>
            <ReleaseInfo release={releaseData} style={{fontSize: '2em'}}/>
        </div>

        <VotingFieldGroup currentScores={descriptorToScore}/>
    </HeaderMain>;
}
