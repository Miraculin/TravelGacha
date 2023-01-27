const ROLL_HISTORY_KEY = "roll_history";
const MAX_HISTORY_LENGTH = 3;

class Roll {
    static country;
    static image;
    static wiki;

    constructor(country, image, wiki) {
        this.country = country;
        this.image = image;
        this.wiki = wiki;
    }
}

class RollHistory {
    static add(roll) {
        // Add to roll history
        let rolls = this.getAll();
        rolls.push(roll);

        // Cap history to last n rolls
        if (rolls.length > MAX_HISTORY_LENGTH) {
            rolls = rolls.splice(rolls.length - MAX_HISTORY_LENGTH);
        }

        // Store in browser local storage
        localStorage.setItem(ROLL_HISTORY_KEY, JSON.stringify(rolls));
    }

    static clear() {
        localStorage.removeItem(ROLL_HISTORY_KEY);
    }

    static getAll() {
        // Retrieve roll history and init array if nothing exists yet
        const history = localStorage.getItem(ROLL_HISTORY_KEY);
        return history ? JSON.parse(history) : [];
    }

    static render() {
        const container = document.getElementById("history");
        const rolls = this.getAll();
        rolls.forEach((roll) => {
            const { country, image, wiki } = roll;

            const span = document.createElement("span");
            span.className = "name";
            span.title = country;
            span.innerText = country;

            const card = document.createElement("div");
            card.className = "card centered";
            card.style.backgroundImage = `url("${image}")`;

            const anchor = document.createElement("a");
            anchor.href = wiki;
            anchor.target = "_blank";
            anchor.rel = "noreferrer";

            card.appendChild(span);
            anchor.appendChild(card);
            container.appendChild(anchor);
        }); 
    }
}
