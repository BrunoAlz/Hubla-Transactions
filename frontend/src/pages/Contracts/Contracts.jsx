import ContractForm from "../../components/ContractForm";
import Layout from "../Layout";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { contractsList } from "../../slices/contracts/contractsSlice";
import ContractStatus from "../../components/ContractStatus";
import { Link, useNavigate, Navigate } from "react-router-dom";

const Contracts = () => {
  const { contracts, isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.contracts
  );

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(contractsList());
  }, []);

  return (
    <div>
      <Layout />
      <div className="container-fluid">
        <div className="row">
          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h1>Contracts</h1>
            <table className="table table-striped table-sm table-hover text-center mt-5">
              <thead>
                <tr className="fw-bold fs-5">
                  <th>N°</th>
                  <th>Date</th>
                  <th>File</th>
                  <th>Owner</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {contracts.map((contract) => (
                  <tr key={contract.id}>
                    <th scope="row">{contract.id}</th>
                    <td>{contract.created_at}</td>
                    <td>{contract.upload}</td>
                    <td className="fw-bold">
                      {contract.first_name} {contract.last_name}
                    </td>
                    <td>
                      <ContractStatus props={contract.status} />
                    </td>
                    <td>
                      <Link to={`${contract.id}`}>Transactions</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Contracts;
