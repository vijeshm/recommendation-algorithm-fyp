#ifndef COMPUTESIMILARITY_H
#define COMPUTESIMILARITY_H

#include <QWidget>
#include <QProcess>

namespace Ui {
class computesimilarity;
}

class computesimilarity : public QWidget
{
    Q_OBJECT
    
public:
    QProcess *proc;
    QProcess *showproc;
    explicit computesimilarity(QWidget *parent = 0);
    ~computesimilarity();
    
private:
    Ui::computesimilarity *ui;

public slots:
    void movenext();
    void moveback();
    void computesimilarityslot();
    void computeover();
    void showover();
    void showclick();
    void zoom();

signals:
    void movetoclusterusers();
    void movebacktoreducedimension();

};

#endif // COMPUTESIMILARITY_H
