import React, { useState } from "react";
import { useNavigate, Link } from 'react-router-dom';

//need to get data from backend

function Matching() {

    return (
        <div>
            <table>
                <tr>
                    <th>Term1</th>
                    <th>Term2</th>
                    <th>Term3</th>
                </tr>
                <tr>
                    <th>Definition1</th>
                    <th>Definition2</th>
                    <th>Definition3</th>
                </tr>
            </table>
        </div>
    )

}

export default Matching;