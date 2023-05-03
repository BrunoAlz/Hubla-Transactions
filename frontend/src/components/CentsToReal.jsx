const CentsToReal = ({ cents }) => {
  function balanceFormatter(cents) {

    let formated_balance = parseFloat(cents) / 100;
    return `R$ ${formated_balance.toFixed(2)}`;
  }

  const formated_balance = balanceFormatter(cents);

  return <>{formated_balance}</>;
};

export default CentsToReal;
