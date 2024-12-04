async function fetchData() {
    const url = 'https://sportscore1.p.rapidapi.com/sports';
    const options = {
	    method: 'GET',
	    headers: {
		    'x-rapidapi-key': '5b9d04ef7emsh2a23a0e65437b46p1bd2a8jsnddcab2d7af28',
		    'x-rapidapi-host': 'sportscore1.p.rapidapi.com'
	    }
    };

    try {
	    const response = await fetch(url, options);
	    if (!response.ok) {
            throw new Error('HTTP Error! status: ${response.status}');
        }
        const result = await response.json();
	    console.log(result);

        const sports = result.data;

        const ul = document.createElement('ul');

        sports.forEach(sport => {
            const li = document.createElement('li');
            li.textContent = sport.name;
            ul.appendChild(li);
        });

        const sportsContainer = document.getElementById('sports');
        sportsContainer.innerHTML = '';
        sportsContainer.appendChild(ul);

        const sportSelect = document.getElementById('sportSelect');
        sportSelect.innerHTML = '<option value="">Select a sport</option>';
        sports.forEach(sport => {
            const option =  document.createElement('option');
            option.value = sport.id;
            option.textContent = sport.name;
            sportSelect.appendChild(option);
        });
        sportSelect.style.display = 'block';
    } catch (error) {
	    console.error('Error fetching sports:', error);
    }
}

const venueCache = {};

async function fetchVenue(venueID) {
    console.log('Fetching venue for ID:', venueId);
    if (!venueID) {
        console.error('Invlaid venue ID');
        return null;
    }
    
    if (venueCache[venueID]) {
        return venueCache[venueID];
    }

    const url = `https://sportscore1.p.rapidapi.com/venues/${venueId}`;
    const options = {
        method: 'GET',
        headers: {
            'x-rapidapi-key': '5b9d04ef7emsh2a23a0e65437b46p1bd2a8jsnddcab2d7af28',
            'x-rapidapi-host': 'sportscore1.p.rapidapi.com'
        }
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error('HTTP Error! status: ${response.status}');
        }
        const result = await response.json();
        venueCache[venueId] = result.data;
        return result.data;
    } catch (error) {
        console.error('Error fetching venue:', error);
        return null;
    }
}


async function fetchRealTimeEvents(sportId) {
    const url = `https://sportscore1.p.rapidapi.com/sports/${sportId}/events`;
    const options = {
	    method: 'GET',
	    headers: {
		    'x-rapidapi-key': '5b9d04ef7emsh2a23a0e65437b46p1bd2a8jsnddcab2d7af28',
		    'x-rapidapi-host': 'sportscore1.p.rapidapi.com'
	    }
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP Error! status: ${response.status}`);
        }
        const result = await response.json();
        console.log(result);

        const matches = result.data;

        const table = document.createElement('table');
        table.classList.add('table', 'table-striped', 'table-bordered');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');

        const headerRow = document.createElement('tr');
        const headers = ['Home Team', 'Away Team', 'Start Time', 'Venue'];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);

        for (const event of matches) {
            const row = document.createElement('tr');
            row.addEventListener('click', () => displayEventDetails(event));

            const homeTeamCell = document.createElement('td');
            homeTeamCell.textContent = event.home_team.name;
            row.appendChild(homeTeamCell);

            const awayTeamCell = document.createElement('td');
            awayTeamCell.textContent = event.away_team.name;
            row.appendChild(awayTeamCell);

            const startTimeCell = document.createElement('td');
            startTimeCell.textContent = event.start_time;
            row.appendChild(startTimeCell);

            const venueCell = document.createElement('td');
            const viewButton = document.createElement('button');
            viewButton.textContent = 'Click to view';
            viewButton.classList.add('btn', 'btn-info');
            viewButton.addEventListener('click', () => displayEventDetails(event));
            venueCell.appendChild(viewButton);
            row.appendChild(venueCell);

            tbody.appendChild(row);
        }

        table.appendChild(thead);
        table.appendChild(tbody);

        const matchesContainer = document.getElementById('matches');
        matchesContainer.innerHTML = '';
        matchesContainer.appendChild(table);
    } catch (error) {
        console.error('Error fetching real-time events:', error);
    }
}

async function displayEventDetails(event) {
    console.log('Displaying event details:', event);
    console.log('Venue ID:', event.venue_Id);
    const venue = await fetchVenue(event.venueID);
    const venueName = venue ? venue.name : 'Unknown';

    const detailsContainer = document.getElementById('eventDetails');
    if (!detailsContainer) {
        console.error('Event details container not found');
        return;
    }

    detailsContainer.innerHTML = `
        <h3>Event Details</h3>
        <p><strong>Home Team:</strong> ${event.home_team.name}</p>
        <p><strong>Away Team:</strong> ${event.away_team.name}</p>
        <p><strong>Start Time:</strong> ${event.start_time}</p>
        <p><strong>Venue:</strong> ${venueName}</p>
    `;
}

document.getElementById('fetchButton').addEventListener('click', fetchData);
document.getElementById('sportSelect').addEventListener('change', (event) => {
    const sportId = event.target.value;
    if (sportId) {
        fetchRealTimeEvents(sportId);
    }
});










