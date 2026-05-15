#!/usr/bin/env node

const { phase2 } = require('../dasheng-daily-phase2/index');

async function clustering(intakeRecordsFile, options = {}) {
  return phase2(intakeRecordsFile, options);
}

if (require.main === module) {
  const intakeRecordsFile = process.argv[2];
  clustering(intakeRecordsFile)
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    })
    .catch(err => {
      console.error(err.message);
      process.exit(1);
    });
}

module.exports = { clustering };
